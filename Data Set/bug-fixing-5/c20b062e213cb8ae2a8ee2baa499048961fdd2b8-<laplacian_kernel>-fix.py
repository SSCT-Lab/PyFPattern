def laplacian_kernel(X, Y=None, gamma=None):
    'Compute the laplacian kernel between X and Y.\n\n    The laplacian kernel is defined as::\n\n        K(x, y) = exp(-gamma ||x-y||_1)\n\n    for each pair of rows x in X and y in Y.\n    Read more in the :ref:`User Guide <laplacian_kernel>`.\n\n    .. versionadded:: 0.17\n\n    Parameters\n    ----------\n    X : array of shape (n_samples_X, n_features)\n\n    Y : array of shape (n_samples_Y, n_features)\n\n    gamma : float, default None\n        If None, defaults to 1.0 / n_features\n\n    Returns\n    -------\n    kernel_matrix : array of shape (n_samples_X, n_samples_Y)\n    '
    (X, Y) = check_pairwise_arrays(X, Y)
    if (gamma is None):
        gamma = (1.0 / X.shape[1])
    K = ((- gamma) * manhattan_distances(X, Y))
    np.exp(K, K)
    return K