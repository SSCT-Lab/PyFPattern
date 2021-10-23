

def __init__(self, module, device_ids=None, output_device=None, dim=0, broadcast_buffers=True):
    super(DistributedDataParallel, self).__init__()
    if (device_ids is None):
        device_ids = list(range(torch.cuda.device_count()))
    if (output_device is None):
        output_device = device_ids[0]
    self.dim = dim
    self.module = module
    self.device_ids = device_ids
    self.output_device = output_device
    self.broadcast_buffers = broadcast_buffers
    self.need_reduction = False
    MB = (1024 * 1024)
    self.broadcast_bucket_size = (10 * MB)
    self.nccl_reduce_bucket_size = (256 * MB)
    module_states = list(self.module.state_dict().values())
    if (len(module_states) > 0):
        self._dist_broadcast_coalesced(module_states, self.broadcast_bucket_size)
    if (len(device_ids) > 1):
        self._module_copies = replicate(self.module, self.device_ids, detach=True)
        self._module_copies[0] = self.module
        for module_copy in self._module_copies[1:]:
            for (param, copy_param) in zip(self.module.parameters(), module_copy.parameters()):
                copy_param.requires_grad = param.requires_grad
    else:
        self._module_copies = [self.module]
    if (dist._backend == dist.dist_backend.NCCL):
        self._register_nccl_grad_hook()
        return
    bucket_bytes_cap = (1 * MB)
    param_buckets = []
    for (dev_idx, module) in enumerate(self._module_copies):
        param_buckets.append(list(_take_tensors(module.parameters(), bucket_bytes_cap)))
    self.bucket_sizes = []
    self.bucket_map = {
        
    }
    for (bucket_idx, param_buckets_tuple) in enumerate(zip(*param_buckets)):
        self.bucket_sizes.append(0)
        for (idx, param_tuple) in enumerate(zip(*param_buckets_tuple)):
            if (idx == 0):
                bucket_param_type = param_tuple[0].type()
                if ((bucket_param_type == torch.cuda.HalfTensor) and (dist._backend != dist.dist_backend.GLOO)):
                    raise RuntimeError('DistributedDataParallel currently only supports half precision parameters with Nccl and Gloo backend')
            if (not param_tuple[0].requires_grad):
                continue
            for p in param_tuple:
                self.bucket_map[p] = bucket_idx
            self.bucket_sizes[bucket_idx] += 1
    self.buckets = [[[] for _ in range(len(self.device_ids))] for _ in range(len(self.bucket_sizes))]
    self.bucket_events = [([None] * len(self.device_ids)) for _ in range(len(self.bucket_sizes))]
    self.reduced = ([False] * len(self.bucket_sizes))
    self._register_grad_hooks()
    self.dispatch_lock = threading.Lock()
    self._start_reduction_threads()
