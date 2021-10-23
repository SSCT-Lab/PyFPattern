def medfilt(volume, kernel_size=None):
    '\n    Perform a median filter on an N-dimensional array.\n\n    Apply a median filter to the input array using a local window-size\n    given by `kernel_size`. The array will automatically be zero-padded.\n\n    Parameters\n    ----------\n    volume : array_like\n        An N-dimensional input array.\n    kernel_size : array_like, optional\n        A scalar or an N-length list giving the size of the median filter\n        window in each dimension.  Elements of `kernel_size` should be odd.\n        If `kernel_size` is a scalar, then this scalar is used as the size in\n        each dimension. Default size is 3 for each dimension.\n\n    Returns\n    -------\n    out : ndarray\n        An array the same size as input containing the median filtered\n        result.\n\n    See also\n    --------\n    scipy.ndimage.median_filter\n\n    Notes\n    -------\n    The more general function `scipy.ndimage.median_filter` has a more\n    efficient implementation of a median filter and therefore runs much faster.\n    '
    volume = atleast_1d(volume)
    if (kernel_size is None):
        kernel_size = ([3] * volume.ndim)
    kernel_size = asarray(kernel_size)
    if (kernel_size.shape == ()):
        kernel_size = np.repeat(kernel_size.item(), volume.ndim)
    for k in range(volume.ndim):
        if ((kernel_size[k] % 2) != 1):
            raise ValueError('Each element of kernel_size should be odd.')
    domain = ones(kernel_size)
    numels = prod(kernel_size, axis=0)
    order = (numels // 2)
    return sigtools._order_filterND(volume, domain, order)