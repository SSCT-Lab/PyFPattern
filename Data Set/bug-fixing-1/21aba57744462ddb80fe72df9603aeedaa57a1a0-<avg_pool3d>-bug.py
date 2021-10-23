

def avg_pool3d(g, input, kernel_size, stride, padding, ceil_mode, count_include_pad):
    if ceil_mode:
        return _unimplemented('avg_pool3d', 'ceil_mode')
    if (not stride):
        stride = kernel_size
    return g.op('AveragePool', input, kernel_shape_i=_triple(kernel_size), strides_i=_triple(stride), pads_i=_triple(padding))
