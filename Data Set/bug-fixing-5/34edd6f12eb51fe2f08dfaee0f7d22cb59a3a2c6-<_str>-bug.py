def _str(self):
    if self.is_sparse:
        size_str = str(tuple(self.shape)).replace(' ', '')
        return '{} of size {} with indices:\n{}and values:\n{}'.format(self.type(), size_str, self._indices(), self._values())
    prefix = 'tensor('
    indent = len(prefix)
    summarize = (self.numel() > PRINT_OPTS.threshold)
    suffix = ')'
    if (not torch._C._is_default_type_cuda()):
        if (self.device.type == 'cuda'):
            suffix = (((", device='" + str(self.device)) + "'") + suffix)
    elif ((self.device.type == 'cpu') or (torch.cuda.current_device() != self.device.index)):
        suffix = (((", device='" + str(self.device)) + "'") + suffix)
    if ((self.dtype != torch.get_default_dtype()) and (self.dtype != torch.int64)):
        suffix = ((', dtype=' + str(self.dtype)) + suffix)
    if (self.numel() == 0):
        tensor_str = '[]'
    else:
        (fmt, scale, sz) = _number_format(self)
        if (scale != 1):
            prefix = ((prefix + SCALE_FORMAT.format(scale)) + (' ' * indent))
        tensor_str = _tensor_str(self, indent, fmt, scale, sz, summarize)
    return ((prefix + tensor_str) + suffix)