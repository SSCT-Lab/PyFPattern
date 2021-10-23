def full2sparse_clipped(vec, topn, eps=1e-09):
    '\n    Like `full2sparse`, but only return the `topn` elements of the greatest magnitude (abs).\n\n    '
    if (topn <= 0):
        return []
    vec = np.asarray(vec, dtype=float)
    nnz = np.nonzero((abs(vec) > eps))[0]
    biggest = nnz.take(argsort(abs(vec).take(nnz), topn, reverse=True))
    return list(zip(biggest, vec.take(biggest)))