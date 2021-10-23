def full2sparse(vec, eps=1e-09):
    '\n    Convert a dense np array into the sparse document format (sequence of 2-tuples).\n\n    Values of magnitude < `eps` are treated as zero (ignored).\n\n    This is the mirror function to `sparse2full`.\n\n    '
    vec = np.asarray(vec, dtype=float)
    nnz = np.nonzero((abs(vec) > eps))[0]
    return list(zip(nnz, vec.take(nnz)))