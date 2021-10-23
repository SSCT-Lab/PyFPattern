def _validate_inputs(image, markers, mask):
    "Ensure that all inputs to watershed have matching shapes and types.\n\n    Parameters\n    ----------\n    image : array\n        The input image.\n    markers : int or array of int\n        The marker image.\n    mask : array, or None\n        A boolean mask, True where we want to compute the watershed.\n\n    Returns\n    -------\n    image, markers, mask : arrays\n        The validated and formatted arrays. Image will have dtype float64,\n        markers int32, and mask int8. If ``None`` was given for the mask,\n        it is a volume of all 1s.\n\n    Raises\n    ------\n    ValueError\n        If the shapes of the given arrays don't match.\n    "
    if (not isinstance(markers, (np.ndarray, list, tuple))):
        markers = regular_seeds(image.shape, markers)
    elif (markers.shape != image.shape):
        raise ValueError(('Markers (shape %s) must have same shape as image (shape %s)' % (markers.ndim, image.ndim)))
    if ((mask is not None) and (mask.shape != image.shape)):
        raise ValueError('mask must have same shape as image')
    if (mask is None):
        mask = np.ones(image.shape, bool)
    return (image.astype(np.float64), markers.astype(np.int32), mask.astype(np.int8))