def adjust_sigmoid(image, cutoff=0.5, gain=10, inv=False):
    'Performs Sigmoid Correction on the input image.\n\n    Also known as Contrast Adjustment.\n    This function transforms the input image pixelwise according to the\n    equation ``O = 1/(1 + exp*(gain*(cutoff - I)))`` after scaling each pixel\n    to the range 0 to 1.\n\n    Parameters\n    ----------\n    image : ndarray\n        Input image.\n    cutoff : float, optional\n        Cutoff of the sigmoid function that shifts the characteristic curve\n        in horizontal direction. Default value is 0.5.\n    gain : float, optional\n        The constant multiplier in exponential\'s power of sigmoid function.\n        Default value is 10.\n    inv : bool, optional\n        If True, returns the negative sigmoid correction. Defaults to False.\n\n    Returns\n    -------\n    out : ndarray\n        Sigmoid corrected output image.\n\n    See Also\n    --------\n    adjust_gamma\n\n    References\n    ----------\n    .. [1] Gustav J. Braun, "Image Lightness Rescaling Using Sigmoidal Contrast\n           Enhancement Functions",\n           http://www.cis.rit.edu/fairchild/PDFs/PAP07.pdf\n\n    '
    _assert_non_negative(image)
    dtype = image.dtype.type
    scale = float((dtype_limits(image, True)[1] - dtype_limits(image, True)[0]))
    if inv:
        out = ((1 - (1 / (1 + np.exp((gain * (cutoff - (image / scale))))))) * scale)
        return dtype(out)
    out = ((1 / (1 + np.exp((gain * (cutoff - (image / scale)))))) * scale)
    return dtype(out)