def rbf_kernel(X, Y=None, gamma=None):
    '\n    Compute the rbf (gaussian) kernel between X and Y::\n\n        K(x, y) = exp(-gamma ||x-y||^2)\n\n    for each pair of rows x in X and y in Y.\n\n    Read more in the :ref:`User Guide <rbf_kernel>`.\n\n    Parameters\n    ----------\n    X : array of shape (n_samples_X, n_features)\n\n    Y : array of shape (n_samples_Y, n_features)\n\n    gamma : float, default None\n        If None, defaults to 1.0 / n_features\n\n    Returns\n    -------\n    kernel_matrix : array of shape (n_samples_X, n_samples_Y)\n    '
    (X, Y) = check_pairwise_arrays(X, Y)
    if (gamma is None):
        gamma = (1.0 / X.shape[1])
    K = euclidean_distances(X, Y, squared=True)
    K *= (- gamma)
    np.exp(K, K)
    return K