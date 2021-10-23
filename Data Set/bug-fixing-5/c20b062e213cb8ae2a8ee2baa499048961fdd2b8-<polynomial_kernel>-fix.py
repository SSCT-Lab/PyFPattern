def polynomial_kernel(X, Y=None, degree=3, gamma=None, coef0=1):
    '\n    Compute the polynomial kernel between X and Y::\n\n        K(X, Y) = (gamma <X, Y> + coef0)^degree\n\n    Read more in the :ref:`User Guide <polynomial_kernel>`.\n\n    Parameters\n    ----------\n    X : ndarray of shape (n_samples_1, n_features)\n\n    Y : ndarray of shape (n_samples_2, n_features)\n\n    degree : int, default 3\n\n    gamma : float, default None\n        if None, defaults to 1.0 / n_features\n\n    coef0 : int, default 1\n\n    Returns\n    -------\n    Gram matrix : array of shape (n_samples_1, n_samples_2)\n    '
    (X, Y) = check_pairwise_arrays(X, Y)
    if (gamma is None):
        gamma = (1.0 / X.shape[1])
    K = safe_sparse_dot(X, Y.T, dense_output=True)
    K *= gamma
    K += coef0
    K **= degree
    return K