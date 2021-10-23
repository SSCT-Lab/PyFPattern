def __init__(self, module, device_ids=None, output_device=None, dim=0):
    super(DistributedDataParallel, self).__init__()
    if (device_ids is None):
        device_ids = list(range(torch.cuda.device_count()))
    if (output_device is None):
        output_device = device_ids[0]
    self.dim = dim
    self.module = module
    self.device_ids = device_ids
    self.output_device = output_device
    for p in self.module.state_dict().values():
        dist.broadcast(p, 0)
    if (len(device_ids) > 1):
        self._module_copies = replicate(self.module, self.device_ids)
        self._module_copies[0] = self.module
        for module_copy in self._module_copies[1:]:
            for (param, copy_param) in zip(self.module.parameters(), module_copy.parameters()):
                copy_param.detach_()
                copy_param.requires_grad = param.requires_grad
    else:
        self._module_copies = [self.module]
    t = None
    for p in self.module.parameters():
        tp = type(p.data)
        if ((t is not None) and (t is not tp)):
            raise ValueError("DistributedDataParallel requires all parameters' data to be of the same type")
        t = tp
    self.bucket_sizes = []
    self.bucket_map = {
        
    }
    MB = (1024 * 1024)
    self.broadcast_bucket_size = (10 * MB)
    bucket_bytes_cap = (1 * MB)
    bucket_bytes = bucket_bytes_cap
    for param_tuple in zip(*map((lambda m: m.parameters()), self._module_copies)):
        if (bucket_bytes >= bucket_bytes_cap):
            self.bucket_sizes.append(0)
            bucket_bytes = 0
        self.bucket_sizes[(- 1)] += 1
        for p in param_tuple:
            self.bucket_map[p] = (len(self.bucket_sizes) - 1)
        bucket_bytes += (p.numel() * p.element_size())
    self.buckets = [[[] for _ in range(len(self.device_ids))] for _ in range(len(self.bucket_sizes))]
    self.bucket_events = [([None] * len(self.device_ids)) for _ in range(len(self.bucket_sizes))]
    self.reduced = ([False] * len(self.bucket_sizes))
    self._register_grad_hooks()
    self.dispatch_lock = threading.Lock()
    self._start_reduction_threads()