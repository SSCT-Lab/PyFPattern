

def distance_transform_bf(input, metric='euclidean', sampling=None, return_distances=True, return_indices=False, distances=None, indices=None):
    "\n    Distance transform function by a brute force algorithm.\n\n    This function calculates the distance transform of the `input`, by\n    replacing each foreground (non-zero) element, with its\n    shortest distance to the background (any zero-valued element).\n\n    In addition to the distance transform, the feature transform can\n    be calculated. In this case the index of the closest background\n    element is returned along the first axis of the result.\n\n    Parameters\n    ----------\n    input : array_like\n        Input\n    metric : str, optional\n        Three types of distance metric are supported: 'euclidean', 'taxicab'\n        and 'chessboard'.\n    sampling : {int, sequence of ints}, optional\n        This parameter is only used in the case of the euclidean `metric`\n        distance transform.\n\n        The sampling along each axis can be given by the `sampling` parameter\n        which should be a sequence of length equal to the input rank, or a\n        single number in which the `sampling` is assumed to be equal along all\n        axes.\n    return_distances : bool, optional\n        The `return_distances` flag can be used to indicate if the distance\n        transform is returned.\n\n        The default is True.\n    return_indices : bool, optional\n        The `return_indices` flags can be used to indicate if the feature\n        transform is returned.\n\n        The default is False.\n    distances : float64 ndarray, optional\n        Optional output array to hold distances (if `return_distances` is\n        True).\n    indices : int64 ndarray, optional\n        Optional output array to hold indices (if `return_indices` is True).\n\n    Returns\n    -------\n    distances : ndarray\n        Distance array if `return_distances` is True.\n    indices : ndarray\n        Indices array if `return_indices` is True.\n\n    Notes\n    -----\n    This function employs a slow brute force algorithm, see also the\n    function distance_transform_cdt for more efficient taxicab and\n    chessboard algorithms.\n\n    "
    if ((not return_distances) and (not return_indices)):
        msg = 'at least one of distances/indices must be specified'
        raise RuntimeError(msg)
    tmp1 = (numpy.asarray(input) != 0)
    struct = generate_binary_structure(tmp1.ndim, tmp1.ndim)
    tmp2 = binary_dilation(tmp1, struct)
    tmp2 = numpy.logical_xor(tmp1, tmp2)
    tmp1 = (tmp1.astype(numpy.int8) - tmp2.astype(numpy.int8))
    metric = metric.lower()
    if (metric == 'euclidean'):
        metric = 1
    elif (metric in ['taxicab', 'cityblock', 'manhattan']):
        metric = 2
    elif (metric == 'chessboard'):
        metric = 3
    else:
        raise RuntimeError('distance metric not supported')
    if (sampling is not None):
        sampling = _ni_support._normalize_sequence(sampling, tmp1.ndim)
        sampling = numpy.asarray(sampling, dtype=numpy.float64)
        if (not sampling.flags.contiguous):
            sampling = sampling.copy()
    if return_indices:
        ft = numpy.zeros(tmp1.shape, dtype=numpy.int32)
    else:
        ft = None
    if return_distances:
        if (distances is None):
            if (metric == 1):
                dt = numpy.zeros(tmp1.shape, dtype=numpy.float64)
            else:
                dt = numpy.zeros(tmp1.shape, dtype=numpy.uint32)
        else:
            if (distances.shape != tmp1.shape):
                raise RuntimeError('distances array has wrong shape')
            if (metric == 1):
                if (distances.dtype.type != numpy.float64):
                    raise RuntimeError('distances array must be float64')
            elif (distances.dtype.type != numpy.uint32):
                raise RuntimeError('distances array must be uint32')
            dt = distances
    else:
        dt = None
    _nd_image.distance_transform_bf(tmp1, metric, sampling, dt, ft)
    if return_indices:
        if isinstance(indices, numpy.ndarray):
            if (indices.dtype.type != numpy.int32):
                raise RuntimeError('indices must of int32 type')
            if (indices.shape != ((tmp1.ndim,) + tmp1.shape)):
                raise RuntimeError('indices has wrong shape')
            tmp2 = indices
        else:
            tmp2 = numpy.indices(tmp1.shape, dtype=numpy.int32)
        ft = numpy.ravel(ft)
        for ii in range(tmp2.shape[0]):
            rtmp = numpy.ravel(tmp2[(ii, ...)])[ft]
            rtmp.shape = tmp1.shape
            tmp2[(ii, ...)] = rtmp
        ft = tmp2
    result = []
    if (return_distances and (not isinstance(distances, numpy.ndarray))):
        result.append(dt)
    if (return_indices and (not isinstance(indices, numpy.ndarray))):
        result.append(ft)
    if (len(result) == 2):
        return tuple(result)
    elif (len(result) == 1):
        return result[0]
    else:
        return None
