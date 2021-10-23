def intensity_range(image, range_values='image', clip_negative=False):
    "Return image intensity range (min, max) based on desired value type.\n\n    Parameters\n    ----------\n    image : array\n        Input image.\n    range_values : str or 2-tuple\n        The image intensity range is configured by this parameter.\n        The possible values for this parameter are enumerated below.\n\n        'image'\n            Return image min/max as the range.\n        'dtype'\n            Return min/max of the image's dtype as the range.\n        dtype-name\n            Return intensity range based on desired `dtype`. Must be valid key\n            in `DTYPE_RANGE`. Note: `image` is ignored for this range type.\n        2-tuple\n            Return `range_values` as min/max intensities. Note that there's no\n            reason to use this function if you just want to specify the\n            intensity range explicitly. This option is included for functions\n            that use `intensity_range` to support all desired range types.\n\n    clip_negative : bool\n        If True, clip the negative range (i.e. return 0 for min intensity)\n        even if the image dtype allows negative values.\n    "
    if (range_values == 'dtype'):
        range_values = image.dtype.type
    if (range_values == 'image'):
        i_min = np.min(image)
        i_max = np.max(image)
    elif (range_values in DTYPE_RANGE):
        (i_min, i_max) = DTYPE_RANGE[range_values]
        if clip_negative:
            i_min = 0
    else:
        (i_min, i_max) = range_values
    return (i_min, i_max)