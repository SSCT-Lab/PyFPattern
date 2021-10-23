def medfilt2d(input, kernel_size=3):
    '\n    Median filter a 2-dimensional array.\n\n    Apply a median filter to the `input` array using a local window-size\n    given by `kernel_size` (must be odd). The array is zero-padded\n    automatically.\n\n    Parameters\n    ----------\n    input : array_like\n        A 2-dimensional input array.\n    kernel_size : array_like, optional\n        A scalar or a list of length 2, giving the size of the\n        median filter window in each dimension.  Elements of\n        `kernel_size` should be odd.  If `kernel_size` is a scalar,\n        then this scalar is used as the size in each dimension.\n        Default is a kernel of size (3, 3).\n\n    Returns\n    -------\n    out : ndarray\n        An array the same size as input containing the median filtered\n        result.\n\n    See also\n    --------\n    scipy.ndimage.median_filter\n\n    Notes\n    -------\n    The more general function `scipy.ndimage.median_filter` has a more\n    efficient implementation of a median filter and therefore runs much faster.\n    '
    image = asarray(input)
    if (kernel_size is None):
        kernel_size = ([3] * 2)
    kernel_size = asarray(kernel_size)
    if (kernel_size.shape == ()):
        kernel_size = np.repeat(kernel_size.item(), 2)
    for size in kernel_size:
        if ((size % 2) != 1):
            raise ValueError('Each element of kernel_size should be odd.')
    return sigtools._medfilt2d(image, kernel_size)