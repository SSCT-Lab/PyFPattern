def rescale(image, scale, order=1, mode=None, cval=0, clip=True, preserve_range=False):
    "Scale image by a certain factor.\n\n    Performs interpolation to upscale or down-scale images. For down-sampling\n    N-dimensional images with integer factors by applying the arithmetic sum or\n    mean, see `skimage.measure.local_sum` and\n    `skimage.transform.downscale_local_mean`, respectively.\n\n    Parameters\n    ----------\n    image : ndarray\n        Input image.\n    scale : {float, tuple of floats}\n        Scale factors. Separate scale factors can be defined as\n        `(row_scale, col_scale)`.\n\n    Returns\n    -------\n    scaled : ndarray\n        Scaled version of the input.\n\n    Other parameters\n    ----------------\n    order : int, optional\n        The order of the spline interpolation, default is 1. The order has to\n        be in the range 0-5. See `skimage.transform.warp` for detail.\n    mode : {'constant', 'edge', 'symmetric', 'reflect', 'wrap'}, optional\n        Points outside the boundaries of the input are filled according\n        to the given mode.  Modes match the behaviour of `numpy.pad`.  The\n        default mode is 'constant'.\n    cval : float, optional\n        Used in conjunction with mode 'constant', the value outside\n        the image boundaries.\n    clip : bool, optional\n        Whether to clip the output to the range of values of the input image.\n        This is enabled by default, since higher order interpolation may\n        produce values outside the given input range.\n    preserve_range : bool, optional\n        Whether to keep the original range of values. Otherwise, the input\n        image is converted according to the conventions of `img_as_float`.\n\n    Examples\n    --------\n    >>> from skimage import data\n    >>> from skimage.transform import rescale\n    >>> image = data.camera()\n    >>> rescale(image, 0.1, mode='reflect').shape\n    (51, 51)\n    >>> rescale(image, 0.5, mode='reflect').shape\n    (256, 256)\n\n    "
    try:
        (row_scale, col_scale) = scale
    except TypeError:
        row_scale = col_scale = scale
    (orig_rows, orig_cols) = (image.shape[0], image.shape[1])
    rows = np.round((row_scale * orig_rows))
    cols = np.round((col_scale * orig_cols))
    output_shape = (rows, cols)
    return resize(image, output_shape, order=order, mode=mode, cval=cval, clip=clip, preserve_range=preserve_range)