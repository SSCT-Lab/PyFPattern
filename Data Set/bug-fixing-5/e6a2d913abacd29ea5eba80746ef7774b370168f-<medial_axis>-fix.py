def medial_axis(image, mask=None, return_distance=False):
    '\n    Compute the medial axis transform of a binary image\n\n    Parameters\n    ----------\n    image : binary ndarray, shape (M, N)\n        The image of the shape to be skeletonized.\n    mask : binary ndarray, shape (M, N), optional\n        If a mask is given, only those elements in `image` with a true\n        value in `mask` are used for computing the medial axis.\n    return_distance : bool, optional\n        If true, the distance transform is returned as well as the skeleton.\n\n    Returns\n    -------\n    out : ndarray of bools\n        Medial axis transform of the image\n    dist : ndarray of ints, optional\n        Distance transform of the image (only returned if `return_distance`\n        is True)\n\n    See also\n    --------\n    skeletonize\n\n    Notes\n    -----\n    This algorithm computes the medial axis transform of an image\n    as the ridges of its distance transform.\n\n    The different steps of the algorithm are as follows\n     * A lookup table is used, that assigns 0 or 1 to each configuration of\n       the 3x3 binary square, whether the central pixel should be removed\n       or kept. We want a point to be removed if it has more than one neighbor\n       and if removing it does not change the number of connected components.\n\n     * The distance transform to the background is computed, as well as\n       the cornerness of the pixel.\n\n     * The foreground (value of 1) points are ordered by\n       the distance transform, then the cornerness.\n\n     * A cython function is called to reduce the image to its skeleton. It\n       processes pixels in the order determined at the previous step, and\n       removes or maintains a pixel according to the lookup table. Because\n       of the ordering, it is possible to process all pixels in only one\n       pass.\n\n    Examples\n    --------\n    >>> square = np.zeros((7, 7), dtype=np.uint8)\n    >>> square[1:-1, 2:-2] = 1\n    >>> square\n    array([[0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0]], dtype=uint8)\n    >>> medial_axis(square).astype(np.uint8)\n    array([[0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 1, 0, 1, 0, 0],\n           [0, 0, 0, 1, 0, 0, 0],\n           [0, 0, 0, 1, 0, 0, 0],\n           [0, 0, 0, 1, 0, 0, 0],\n           [0, 0, 1, 0, 1, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0]], dtype=uint8)\n\n    '
    global _eight_connect
    if (mask is None):
        masked_image = image.astype(np.bool)
    else:
        masked_image = image.astype(bool).copy()
        masked_image[(~ mask)] = False
    center_is_foreground = (np.arange(512) & (2 ** 4)).astype(bool)
    table = (center_is_foreground & (np.array([(ndi.label(_pattern_of(index), _eight_connect)[1] != ndi.label(_pattern_of((index & (~ (2 ** 4)))), _eight_connect)[1]) for index in range(512)]) | np.array([(np.sum(_pattern_of(index)) < 3) for index in range(512)])))
    distance = ndi.distance_transform_edt(masked_image)
    if return_distance:
        store_distance = distance.copy()
    cornerness_table = np.array([(9 - np.sum(_pattern_of(index))) for index in range(512)])
    corner_score = _table_lookup(masked_image, cornerness_table)
    (i, j) = np.mgrid[0:image.shape[0], 0:image.shape[1]]
    result = masked_image.copy()
    distance = distance[result]
    i = np.ascontiguousarray(i[result], dtype=np.intp)
    j = np.ascontiguousarray(j[result], dtype=np.intp)
    result = np.ascontiguousarray(result, np.uint8)
    generator = np.random.RandomState(0)
    tiebreaker = generator.permutation(np.arange(masked_image.sum()))
    order = np.lexsort((tiebreaker, corner_score[masked_image], distance))
    order = np.ascontiguousarray(order, dtype=np.int32)
    table = np.ascontiguousarray(table, dtype=np.uint8)
    _skeletonize_loop(result, i, j, order, table)
    result = result.astype(bool)
    if (mask is not None):
        result[(~ mask)] = image[(~ mask)]
    if return_distance:
        return (result, store_distance)
    else:
        return result