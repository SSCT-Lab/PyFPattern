def ismatrix(m):
    'Check does `m` numpy.ndarray or `scipy.sparse` matrix.\n\n    Parameters\n    ----------\n    m : object\n        Candidate for matrix\n\n    Returns\n    -------\n    bool\n        True if `m` is matrix, False otherwise.\n\n    '
    return ((isinstance(m, np.ndarray) and (m.ndim == 2)) or scipy.sparse.issparse(m))