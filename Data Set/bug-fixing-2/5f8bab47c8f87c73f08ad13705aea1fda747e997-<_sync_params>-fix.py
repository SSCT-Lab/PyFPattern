

def _sync_params(self):
    params = [p.data for p in self.module.parameters()]
    result = broadcast_coalesced(params, self.device_ids, self.broadcast_bucket_size)
    for (tensors, module) in zip(result[1:], self._module_copies[1:]):
        for (tensor, param) in zip(tensors, module.parameters()):
            param.data.set_(tensor)
    buffers = list(self.module._all_buffers())
    if (len(buffers) > 0):
        flat_buffers = _flatten_tensors(buffers)
        dist.broadcast(flat_buffers, 0)
        for (buf, synced) in zip(buffers, _unflatten_tensors(flat_buffers, buffers)):
            buf.copy_(synced)
        result = broadcast_coalesced(buffers, self.device_ids, self.broadcast_bucket_size)
        for (tensors, module) in zip(result[1:], self._module_copies[1:]):
            for (tensor, buf) in zip(tensors, module._all_buffers()):
                buf.set_(tensor)
