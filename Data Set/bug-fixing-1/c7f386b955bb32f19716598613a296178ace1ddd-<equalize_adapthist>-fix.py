

@adapt_rgb(hsv_value)
def equalize_adapthist(image, ntiles_x=None, ntiles_y=None, clip_limit=0.01, nbins=256, kernel_size=None):
    'Contrast Limited Adaptive Histogram Equalization (CLAHE).\n\n    An algorithm for local contrast enhancement, that uses histograms computed\n    over different tile regions of the image. Local details can therefore be\n    enhanced even in regions that are darker or lighter than most of the image.\n\n    Parameters\n    ----------\n    image : array-like\n        Input image.\n    kernel_size: integer or 2-tuple\n        Defines the shape of contextual regions used in the algorithm.\n        If an integer is given, the shape will be a square of\n        sidelength given by this value.\n    ntiles_x : int, optional (deprecated in favor of ``kernel_size``)\n        Number of tile regions in the X direction (horizontal).\n    ntiles_y : int, optional (deprecated in favor of ``kernel_size``)\n        Number of tile regions in the Y direction (vertical).\n    clip_limit : float: optional\n        Clipping limit, normalized between 0 and 1 (higher values give more\n        contrast).\n    nbins : int, optional\n        Number of gray bins for histogram ("dynamic range").\n\n    Returns\n    -------\n    out : ndarray\n        Equalized image.\n\n    See Also\n    --------\n    equalize_hist, rescale_intensity\n\n    Notes\n    -----\n    * For color images, the following steps are performed:\n       - The image is converted to HSV color space\n       - The CLAHE algorithm is run on the V (Value) channel\n       - The image is converted back to RGB space and returned\n    * For RGBA images, the original alpha channel is removed.\n\n    References\n    ----------\n    .. [1] http://tog.acm.org/resources/GraphicsGems/\n    .. [2] https://en.wikipedia.org/wiki/CLAHE#CLAHE\n    '
    image = img_as_uint(image)
    image = rescale_intensity(image, out_range=(0, (NR_OF_GREY - 1)))
    if ((ntiles_x is not None) or (ntiles_y is not None)):
        warn('`ntiles_*` have been deprecated in favor of `kernel_size`.  The `ntiles_*` keyword arguments will be removed in v0.14', skimage_deprecation)
    if (kernel_size is None):
        ntiles_x = (ntiles_x or 8)
        ntiles_y = (ntiles_y or 8)
        kernel_size = (np.round((image.shape[0] / ntiles_y)), np.round((image.shape[1] / ntiles_x)))
    if isinstance(kernel_size, numbers.Number):
        kernel_size = (kernel_size, kernel_size)
    kernel_size = [int(k) for k in kernel_size]
    image = _clahe(image, kernel_size, (clip_limit * nbins), nbins)
    image = img_as_float(image)
    return rescale_intensity(image)
