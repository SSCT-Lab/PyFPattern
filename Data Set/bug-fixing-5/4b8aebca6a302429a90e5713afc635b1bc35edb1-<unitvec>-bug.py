def unitvec(vec, norm='l2'):
    '\n    Scale a vector to unit length. The only exception is the zero vector, which\n    is returned back unchanged.\n\n    Output will be in the same format as input (i.e., gensim vector=>gensim vector,\n    or np array=>np array, scipy.sparse=>scipy.sparse).\n    '
    if (norm not in ('l1', 'l2')):
        raise ValueError(("'%s' is not a supported norm. Currently supported norms are 'l1' and 'l2'." % norm))
    if scipy.sparse.issparse(vec):
        vec = vec.tocsr()
        if (norm == 'l1'):
            veclen = np.sum(np.abs(vec.data))
        if (norm == 'l2'):
            veclen = np.sqrt(np.sum((vec.data ** 2)))
        if (veclen > 0.0):
            return (vec / veclen)
        else:
            return vec
    if isinstance(vec, np.ndarray):
        vec = np.asarray(vec, dtype=float)
        if (norm == 'l1'):
            veclen = np.sum(np.abs(vec))
        if (norm == 'l2'):
            veclen = blas_nrm2(vec)
        if (veclen > 0.0):
            return blas_scal((1.0 / veclen), vec)
        else:
            return vec
    try:
        first = next(iter(vec))
    except StopIteration:
        return vec
    if (isinstance(first, (tuple, list)) and (len(first) == 2)):
        if (norm == 'l1'):
            length = float(sum((abs(val) for (_, val) in vec)))
        if (norm == 'l2'):
            length = (1.0 * math.sqrt(sum(((val ** 2) for (_, val) in vec))))
        assert (length > 0.0), 'sparse documents must not contain any explicit zero entries'
        return ret_normalized_vec(vec, length)
    else:
        raise ValueError('unknown input type')