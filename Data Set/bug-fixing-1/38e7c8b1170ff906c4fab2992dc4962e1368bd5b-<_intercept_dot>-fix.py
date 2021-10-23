

def _intercept_dot(w, X, y):
    'Computes y * np.dot(X, w).\n\n    It takes into consideration if the intercept should be fit or not.\n\n    Parameters\n    ----------\n    w : ndarray, shape (n_features,) or (n_features + 1,)\n        Coefficient vector.\n\n    X : {array-like, sparse matrix}, shape (n_samples, n_features)\n        Training data.\n\n    y : ndarray, shape (n_samples,)\n        Array of labels.\n\n    Returns\n    -------\n    w : ndarray, shape (n_features,)\n        Coefficient vector without the intercept weight (w[-1]) if the\n        intercept should be fit. Unchanged otherwise.\n\n    c : float\n        The intercept.\n\n    yz : float\n        y * np.dot(X, w).\n    '
    c = 0.0
    if (w.size == (X.shape[1] + 1)):
        c = w[(- 1)]
        w = w[:(- 1)]
    z = (safe_sparse_dot(X, w) + c)
    yz = (y * z)
    return (w, c, yz)
