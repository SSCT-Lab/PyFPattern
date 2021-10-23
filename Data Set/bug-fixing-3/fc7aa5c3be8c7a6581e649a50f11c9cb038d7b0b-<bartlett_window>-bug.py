def bartlett_window(window_length, periodic=True, dtype=torch.float32):
    'Bartlett window function.\n\n    This method computes the Bartlett window function:\n\n    .. math::\n        w[n] = 1 - \\left| \\frac{2n}{N-1} - 1 \\right| = \\begin{cases}\n            \\frac{2n}{N - 1} & \\text{if } 0 \\leq n \\leq \\frac{N - 1}{2} \\\\\n            2 - \\frac{2n}{N - 1} & \\text{if } \\frac{N - 1}{2} < n < N \\\\\n        \\end{cases}\n\n    , where :math:`N` is the full window size.\n\n    The input :attr:`window_length` is a positive integer controlling the\n    returned window size. :attr:`periodic` flag determines whether the returned\n    window trims off the last duplicate value from the symmetric window and is\n    ready to be used as a periodic window with functions like\n    :meth:`torch.stft`. Therefore, if :attr:`periodic` is true, the :math:`N` in\n    above formula is in fact :math:`\\text{window_length} + 1`. Also, we always have\n    ``torch.bartlett_window(L, periodic=True)`` equal to\n    ``torch.bartlett_window(L + 1, periodic=False)[:-1])``.\n\n    .. note::\n        If :attr:`window_length` :math:`\\leq 2`, the returned window contains a single value 1.\n\n    Arguments:\n        window_length (int): the size of returned window\n        periodic (bool, optional): If True, returns a window to be used as periodic\n            function. If False, return a symmetric window.\n        dtype (torch.dtype, optional): the desired type of returned window.\n            Default: `torch.float32`\n\n    Returns:\n        Tensor: A 1-D tensor of size :math:`(window\\_length)` containing the window\n    '
    if (not dtype.is_floating_point):
        raise ValueError('dtype must be a floating point type, but got dtype={}'.format(dtype))
    if (window_length <= 0):
        raise ValueError('window_length must be positive')
    if (window_length == 1):
        return torch.ones(window_length, dtype=dtype)
    window_length += int(periodic)
    window = torch.arange(window_length, dtype=dtype).mul_((2.0 / (window_length - 1)))
    first_half_size = (((window_length - 1) >> 1) + 1)
    window.narrow(0, first_half_size, (window_length - first_half_size)).mul_((- 1)).add_(2)
    if periodic:
        return window[:(- 1)]
    else:
        return window