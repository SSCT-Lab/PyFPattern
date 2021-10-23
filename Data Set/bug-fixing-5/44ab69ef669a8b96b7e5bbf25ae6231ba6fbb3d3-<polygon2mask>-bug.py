def polygon2mask(image_shape, polygon):
    "Compute a mask from polygon.\n\n    Parameters\n    ----------\n    image_shape : tuple of size 2.\n        The shape of the mask.\n    polygon : array_like.\n        The polygon coordinates of shape (N, 2) where N is\n        the number of points.\n\n    Returns\n    -------\n    mask : 2-D ndarray of type 'bool'.\n        The mask that corresponds to the input polygon.\n\n    Notes\n    -----\n    This function does not do any border checking, so that all\n    the vertices need to be within the given shape.\n\n    Examples\n    --------\n    >>> import numpy as np\n    >>> from skimage.draw import polygon2mask\n    >>> image_shape = (128, 128)\n    >>> polygon = np.array([[60, 100], [100, 40], [40, 40]])\n    >>> mask = polygon2mask(image_shape, polygon)\n    >>> mask.shape\n    (128, 128)\n    "
    polygon = np.asarray(polygon)
    (vertex_row_coords, vertex_col_coords) = polygon.T
    (fill_row_coords, fill_col_coords) = draw.polygon(vertex_row_coords, vertex_col_coords, image_shape)
    mask = np.zeros(image_shape, dtype=np.bool)
    mask[(fill_row_coords, fill_col_coords)] = True
    return mask