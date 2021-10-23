def adjust_log(image, gain=1, inv=False):
    'Performs Logarithmic correction on the input image.\n\n    This function transforms the input image pixelwise according to the\n    equation ``O = gain*log(1 + I)`` after scaling each pixel to the range 0 to 1.\n    For inverse logarithmic correction, the equation is ``O = gain*(2**I - 1)``.\n\n    Parameters\n    ----------\n    image : ndarray\n        Input image.\n    gain : float\n        The constant multiplier. Default value is 1.\n    inv : float\n        If True, it performs inverse logarithmic correction,\n        else correction will be logarithmic. Defaults to False.\n\n    Returns\n    -------\n    out : ndarray\n        Logarithm corrected output image.\n\n    See Also\n    --------\n    adjust_gamma\n\n    References\n    ----------\n    .. [1] http://www.ece.ucsb.edu/Faculty/Manjunath/courses/ece178W03/EnhancePart1.pdf\n\n    '
    _assert_non_negative(image)
    dtype = image.dtype.type
    scale = float((dtype_limits(image, True)[1] - dtype_limits(image, True)[0]))
    if inv:
        out = ((((2 ** (image / scale)) - 1) * scale) * gain)
        return dtype(out)
    out = ((np.log2((1 + (image / scale))) * scale) * gain)
    return dtype(out)