def resize(image, output_shape, order=1, mode=None, cval=0, clip=True, preserve_range=False):
    "Resize image to match a certain size.\n\n    Performs interpolation to up-size or down-size images. For down-sampling\n    N-dimensional images by applying the arithmetic sum or mean, see\n    `skimage.measure.local_sum` and `skimage.transform.downscale_local_mean`,\n    respectively.\n\n    Parameters\n    ----------\n    image : ndarray\n        Input image.\n    output_shape : tuple or ndarray\n        Size of the generated output image `(rows, cols[, dim])`. If `dim` is\n        not provided, the number of channels is preserved. In case the number\n        of input channels does not equal the number of output channels a\n        3-dimensional interpolation is applied.\n\n    Returns\n    -------\n    resized : ndarray\n        Resized version of the input.\n\n    Other parameters\n    ----------------\n    order : int, optional\n        The order of the spline interpolation, default is 1. The order has to\n        be in the range 0-5. See `skimage.transform.warp` for detail.\n    mode : {'constant', 'edge', 'symmetric', 'reflect', 'wrap'}, optional\n        Points outside the boundaries of the input are filled according\n        to the given mode.  Modes match the behaviour of `numpy.pad`.  The\n        default mode is 'constant'.\n    cval : float, optional\n        Used in conjunction with mode 'constant', the value outside\n        the image boundaries.\n    clip : bool, optional\n        Whether to clip the output to the range of values of the input image.\n        This is enabled by default, since higher order interpolation may\n        produce values outside the given input range.\n    preserve_range : bool, optional\n        Whether to keep the original range of values. Otherwise, the input\n        image is converted according to the conventions of `img_as_float`.\n\n    Notes\n    -----\n    Modes 'reflect' and 'symmetric' are similar, but differ in whether the edge\n    pixels are duplicated during the reflection.  As an example, if an array\n    has values [0, 1, 2] and was padded to the right by four values using\n    symmetric, the result would be [0, 1, 2, 2, 1, 0, 0], while for reflect it\n    would be [0, 1, 2, 1, 0, 1, 2].\n\n    Examples\n    --------\n    >>> from skimage import data\n    >>> from skimage.transform import resize\n    >>> image = data.camera()\n    >>> resize(image, (100, 100), mode='reflect').shape\n    (100, 100)\n\n    "
    if (mode is None):
        mode = 'constant'
        warn("The default mode, 'constant', will be changed to 'reflect' in skimage 0.15.")
    (rows, cols) = (output_shape[0], output_shape[1])
    (orig_rows, orig_cols) = (image.shape[0], image.shape[1])
    row_scale = (float(orig_rows) / rows)
    col_scale = (float(orig_cols) / cols)
    if ((len(output_shape) == 3) and ((image.ndim == 2) or (output_shape[2] != image.shape[2]))):
        ndi_mode = _to_ndimage_mode(mode)
        dim = output_shape[2]
        if (image.ndim == 2):
            image = image[:, :, np.newaxis]
        orig_dim = image.shape[2]
        dim_scale = (float(orig_dim) / dim)
        (map_rows, map_cols, map_dims) = np.mgrid[:rows, :cols, :dim]
        map_rows = ((row_scale * (map_rows + 0.5)) - 0.5)
        map_cols = ((col_scale * (map_cols + 0.5)) - 0.5)
        map_dims = ((dim_scale * (map_dims + 0.5)) - 0.5)
        coord_map = np.array([map_rows, map_cols, map_dims])
        image = convert_to_float(image, preserve_range)
        out = ndi.map_coordinates(image, coord_map, order=order, mode=ndi_mode, cval=cval)
        _clip_warp_output(image, out, order, mode, cval, clip)
    else:
        if ((rows == 1) and (cols == 1)):
            tform = AffineTransform(translation=(((orig_cols / 2.0) - 0.5), ((orig_rows / 2.0) - 0.5)))
        else:
            src_corners = (np.array([[1, 1], [1, rows], [cols, rows]]) - 1)
            dst_corners = np.zeros(src_corners.shape, dtype=np.double)
            dst_corners[:, 0] = ((col_scale * (src_corners[:, 0] + 0.5)) - 0.5)
            dst_corners[:, 1] = ((row_scale * (src_corners[:, 1] + 0.5)) - 0.5)
            tform = AffineTransform()
            tform.estimate(src_corners, dst_corners)
        out = warp(image, tform, output_shape=output_shape, order=order, mode=mode, cval=cval, clip=clip, preserve_range=preserve_range)
    return out