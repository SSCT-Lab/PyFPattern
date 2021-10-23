def max_pool3d(input, kernel_size, stride=None, padding=0, dilation=1, ceil_mode=False, return_indices=False):
    'Applies a 3D max pooling over an input signal composed of several input\n    planes.\n\n    See :class:`~torch.nn.MaxPool3d` for details.\n    '
    ret = torch._C._nn.max_pool3d(input, kernel_size, stride, padding, dilation, ceil_mode)
    return (ret if return_indices else ret[0])