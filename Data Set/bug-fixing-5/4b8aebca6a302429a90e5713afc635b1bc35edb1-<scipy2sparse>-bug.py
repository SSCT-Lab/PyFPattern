def scipy2sparse(vec, eps=1e-09):
    'Convert a scipy.sparse vector into gensim document format (=list of 2-tuples).'
    vec = vec.tocsr()
    assert (vec.shape[0] == 1)
    return [(int(pos), float(val)) for (pos, val) in zip(vec.indices, vec.data) if (np.abs(val) > eps)]