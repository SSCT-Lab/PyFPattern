

def conv3d(input, weight, bias=None, stride=1, padding=0, dilation=1, groups=1):
    'Applies a 3D convolution over an input image composed of several input\n        planes.\n\n    See :class:`~torch.nn.Conv3d` for details and output shape.\n\n    Args:\n        input: input tensor of shape (minibatch x in_channels x iT x iH x iW)\n        weight: filters tensor of shape (out_channels, in_channels, kT, kH, kW)\n        bias: optional bias tensor of shape (out_channels)\n        stride: the stride of the convolving kernel. Can be a single number or\n          a tuple (st x sh x sw). Default: 1\n        padding: implicit zero padding on the input. Can be a single number or\n          a tuple. Default: 0\n\n    Examples:\n        >>> filters = autograd.Variable(torch.randn(33, 16, 3, 3, 3))\n        >>> inputs = autograd.Variable(torch.randn(20, 16, 50, 10, 20))\n        >>> F.conv3d(inputs)\n    '
    f = ConvNd(_triple(stride), _triple(padding), _triple(dilation), False, _triple(0), groups)
    return (f(input, weight, bias) if (bias is not None) else f(input, weight))
