def hamming_window(window_length, periodic=True, alpha=0.54, beta=0.46, dtype=torch.float32):
    'Hamming window function.\n\n    This method computes the Hamming window function:\n\n    .. math::\n        w[n] = \\alpha - \\beta\\ \\cos \\left( \\frac{2 \\pi n}{N - 1} \\right)\n\n    where :math:`N` is the full window size.\n\n    The input :attr:`window_length` is a positive integer controlling the\n    returned window size. :attr:`periodic` flag determines whether the returned\n    window trims off the last duplicate value from the symmetric window and is\n    ready to be used as a periodic window with functions like\n    :meth:`torch.stft`. Therefore, if :attr:`periodic` is true, the :math:`N` in\n    above formula is in fact :math:`\\text{window_length} + 1`. Also, we always have\n    ``torch.hamming_window(L, periodic=True)`` equal to\n    ``torch.hamming_window(L + 1, periodic=False)[:-1])``.\n\n    .. note::\n        If :attr:`window_length` :math:`\\leq 2`, the returned window contains a single value 1.\n\n    .. note::\n        This is a generalized version of :meth:`torch.hann_window`.\n\n    Arguments:\n        window_length (int): the size of returned window\n        periodic (bool, optional): If True, returns a window to be used as periodic\n            function. If False, return a symmetric window.\n        dtype (torch.dtype, optional): the desired type of returned window.\n            Default: `torch.float32`\n\n    Returns:\n        Tensor: A 1-D tensor of size :math:`(window\\_length)` containing the window\n    '
    if (not dtype.is_floating_point):
        raise ValueError('dtype must be a floating point type, but got dtype={}'.format(dtype))
    if (window_length <= 0):
        raise ValueError('window_length must be positive')
    if (window_length == 1):
        return torch.ones(window_length, dtype=dtype)
    window_length += int(periodic)
    window = torch.arange(window_length, dtype=dtype)
    window = window.mul_(((math.pi * 2) / (window_length - 1))).cos_().mul_((- beta)).add_(alpha)
    if periodic:
        return window[:(- 1)]
    else:
        return window