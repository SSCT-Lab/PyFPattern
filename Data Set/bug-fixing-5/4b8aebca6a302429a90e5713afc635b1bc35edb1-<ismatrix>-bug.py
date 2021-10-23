def ismatrix(m):
    return ((isinstance(m, np.ndarray) and (m.ndim == 2)) or scipy.sparse.issparse(m))