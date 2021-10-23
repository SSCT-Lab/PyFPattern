def adjust_gamma(image, gamma=1, gain=1):
    'Performs Gamma Correction on the input image.\n\n    Also known as Power Law Transform.\n    This function transforms the input image pixelwise according to the\n    equation ``O = I**gamma`` after scaling each pixel to the range 0 to 1.\n\n    Parameters\n    ----------\n    image : ndarray\n        Input image.\n    gamma : float\n        Non negative real number. Default value is 1.\n    gain : float\n        The constant multiplier. Default value is 1.\n\n    Returns\n    -------\n    out : ndarray\n        Gamma corrected output image.\n\n    See Also\n    --------\n    adjust_log\n\n    Notes\n    -----\n    For gamma greater than 1, the histogram will shift towards left and\n    the output image will be darker than the input image.\n\n    For gamma less than 1, the histogram will shift towards right and\n    the output image will be brighter than the input image.\n\n    References\n    ----------\n    .. [1] https://en.wikipedia.org/wiki/Gamma_correction\n\n    Examples\n    --------\n    >>> from skimage import data, exposure, img_as_float\n    >>> image = img_as_float(data.moon())\n    >>> gamma_corrected = exposure.adjust_gamma(image, 2)\n    >>> # Output is darker for gamma > 1\n    >>> image.mean() > gamma_corrected.mean()\n    True\n    '
    _assert_non_negative(image)
    dtype = image.dtype.type
    if (gamma < 0):
        raise ValueError('Gamma should be a non-negative real number.')
    scale = float((dtype_limits(image, True)[1] - dtype_limits(image, True)[0]))
    out = ((((image / scale) ** gamma) * scale) * gain)
    return dtype(out)