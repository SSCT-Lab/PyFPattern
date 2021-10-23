def _path_residuals(X, y, train, test, path, path_params, alphas=None, l1_ratio=1, X_order=None, dtype=None):
    "Returns the MSE for the models computed by 'path'\n\n    Parameters\n    ----------\n    X : {array-like, sparse matrix}, shape (n_samples, n_features)\n        Training data.\n\n    y : array-like, shape (n_samples,) or (n_samples, n_targets)\n        Target values\n\n    train : list of indices\n        The indices of the train set\n\n    test : list of indices\n        The indices of the test set\n\n    path : callable\n        function returning a list of models on the path. See\n        enet_path for an example of signature\n\n    path_params : dictionary\n        Parameters passed to the path function\n\n    alphas : array-like, optional\n        Array of float that is used for cross-validation. If not\n        provided, computed using 'path'.\n\n    l1_ratio : float, optional\n        float between 0 and 1 passed to ElasticNet (scaling between\n        l1 and l2 penalties). For ``l1_ratio = 0`` the penalty is an\n        L2 penalty. For ``l1_ratio = 1`` it is an L1 penalty. For ``0\n        < l1_ratio < 1``, the penalty is a combination of L1 and L2.\n\n    X_order : {'F', 'C', or None}, optional\n        The order of the arrays expected by the path function to\n        avoid memory copies\n\n    dtype : a numpy dtype or None\n        The dtype of the arrays expected by the path function to\n        avoid memory copies\n    "
    X_train = X[train]
    y_train = y[train]
    X_test = X[test]
    y_test = y[test]
    fit_intercept = path_params['fit_intercept']
    normalize = path_params['normalize']
    if (y.ndim == 1):
        precompute = path_params['precompute']
    else:
        precompute = False
    (X_train, y_train, X_offset, y_offset, X_scale, precompute, Xy) = _pre_fit(X_train, y_train, None, precompute, normalize, fit_intercept, copy=False)
    path_params = path_params.copy()
    path_params['Xy'] = Xy
    path_params['X_offset'] = X_offset
    path_params['X_scale'] = X_scale
    path_params['precompute'] = precompute
    path_params['copy_X'] = False
    path_params['alphas'] = alphas
    if ('l1_ratio' in path_params):
        path_params['l1_ratio'] = l1_ratio
    X_train = check_array(X_train, 'csc', dtype=dtype, order=X_order)
    (alphas, coefs, _) = path(X_train, y_train, **path_params)
    del X_train, y_train
    if (y.ndim == 1):
        coefs = coefs[np.newaxis, :, :]
        y_offset = np.atleast_1d(y_offset)
        y_test = y_test[:, np.newaxis]
    if normalize:
        nonzeros = np.flatnonzero(X_scale)
        coefs[:, nonzeros] /= X_scale[nonzeros][:, np.newaxis]
    intercepts = (y_offset[:, np.newaxis] - np.dot(X_offset, coefs))
    X_test_coefs = safe_sparse_dot(X_test, coefs)
    residues = (X_test_coefs - y_test[:, :, np.newaxis])
    residues += intercepts
    this_mses = (residues ** 2).mean(axis=0).mean(axis=0)
    return this_mses