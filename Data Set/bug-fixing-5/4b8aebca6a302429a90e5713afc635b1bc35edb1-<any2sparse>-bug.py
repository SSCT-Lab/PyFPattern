def any2sparse(vec, eps=1e-09):
    'Convert a np/scipy vector into gensim document format (=list of 2-tuples).'
    if isinstance(vec, np.ndarray):
        return dense2vec(vec, eps)
    if scipy.sparse.issparse(vec):
        return scipy2sparse(vec, eps)
    return [(int(fid), float(fw)) for (fid, fw) in vec if (np.abs(fw) > eps)]