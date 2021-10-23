

def _umeyama(src, dst, estimate_scale):
    'Estimate N-D similarity transformation with or without scaling.\n\n    Parameters\n    ----------\n    src : (M, N) array\n        Source coordinates.\n    dst : (M, N) array\n        Destination coordinates.\n    estimate_scale : bool\n        Whether to estimate scaling factor.\n\n    Returns\n    -------\n    T : (N + 1, N + 1)\n        The homogeneous similarity transformation matrix. The matrix contains\n        NaN values only if the problem is not well-conditioned.\n\n    References\n    ----------\n    .. [1] "Least-squares estimation of transformation parameters between two\n            point patterns", Shinji Umeyama, PAMI 1991, DOI: 10.1109/34.88573\n\n    '
    num = src.shape[0]
    dim = src.shape[1]
    src_mean = src.mean(axis=0)
    dst_mean = dst.mean(axis=0)
    src_demean = (src - src_mean)
    dst_demean = (dst - dst_mean)
    A = (np.dot(dst_demean.T, src_demean) / num)
    d = np.ones((dim,), dtype=np.double)
    if (np.linalg.det(A) < 0):
        d[(dim - 1)] = (- 1)
    T = np.eye((dim + 1), dtype=np.double)
    (U, S, V) = np.linalg.svd(A)
    rank = np.linalg.matrix_rank(A)
    if (rank == 0):
        return (np.nan * T)
    elif (rank == (dim - 1)):
        if ((np.linalg.det(U) * np.linalg.det(V)) > 0):
            T[:dim, :dim] = np.dot(U, V)
        else:
            s = d[(dim - 1)]
            d[(dim - 1)] = (- 1)
            T[:dim, :dim] = np.dot(U, np.dot(np.diag(d), V))
            d[(dim - 1)] = s
    else:
        T[:dim, :dim] = np.dot(U, np.dot(np.diag(d), V.T))
    if estimate_scale:
        scale = ((1.0 / src_demean.var(axis=0).sum()) * np.dot(S, d))
    else:
        scale = 1.0
    T[:dim, dim] = (dst_mean - (scale * np.dot(T[:dim, :dim], src_mean.T)))
    T[:dim, :dim] *= scale
    return T
