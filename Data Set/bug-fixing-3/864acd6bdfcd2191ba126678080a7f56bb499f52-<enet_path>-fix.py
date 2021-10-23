def enet_path(X, y, l1_ratio=0.5, eps=0.001, n_alphas=100, alphas=None, precompute='auto', Xy=None, copy_X=True, coef_init=None, verbose=False, return_n_iter=False, positive=False, check_input=True, **params):
    "\n    Compute elastic net path with coordinate descent.\n\n    The elastic net optimization function varies for mono and multi-outputs.\n\n    For mono-output tasks it is::\n\n        1 / (2 * n_samples) * ||y - Xw||^2_2\n        + alpha * l1_ratio * ||w||_1\n        + 0.5 * alpha * (1 - l1_ratio) * ||w||^2_2\n\n    For multi-output tasks it is::\n\n        (1 / (2 * n_samples)) * ||Y - XW||^Fro_2\n        + alpha * l1_ratio * ||W||_21\n        + 0.5 * alpha * (1 - l1_ratio) * ||W||_Fro^2\n\n    Where::\n\n        ||W||_21 = \\sum_i \\sqrt{\\sum_j w_{ij}^2}\n\n    i.e. the sum of norm of each row.\n\n    Read more in the :ref:`User Guide <elastic_net>`.\n\n    Parameters\n    ----------\n    X : {array-like}, shape (n_samples, n_features)\n        Training data. Pass directly as Fortran-contiguous data to avoid\n        unnecessary memory duplication. If ``y`` is mono-output then ``X``\n        can be sparse.\n\n    y : ndarray, shape (n_samples,) or (n_samples, n_outputs)\n        Target values.\n\n    l1_ratio : float, optional\n        Number between 0 and 1 passed to elastic net (scaling between\n        l1 and l2 penalties). ``l1_ratio=1`` corresponds to the Lasso.\n\n    eps : float\n        Length of the path. ``eps=1e-3`` means that\n        ``alpha_min / alpha_max = 1e-3``.\n\n    n_alphas : int, optional\n        Number of alphas along the regularization path.\n\n    alphas : ndarray, optional\n        List of alphas where to compute the models.\n        If None alphas are set automatically.\n\n    precompute : True | False | 'auto' | array-like\n        Whether to use a precomputed Gram matrix to speed up\n        calculations. If set to ``'auto'`` let us decide. The Gram\n        matrix can also be passed as argument.\n\n    Xy : array-like, optional\n        Xy = np.dot(X.T, y) that can be precomputed. It is useful\n        only when the Gram matrix is precomputed.\n\n    copy_X : bool, optional, default True\n        If ``True``, X will be copied; else, it may be overwritten.\n\n    coef_init : array, shape (n_features, ) | None\n        The initial values of the coefficients.\n\n    verbose : bool or int\n        Amount of verbosity.\n\n    return_n_iter : bool\n        Whether to return the number of iterations or not.\n\n    positive : bool, default False\n        If set to True, forces coefficients to be positive.\n        (Only allowed when ``y.ndim == 1``).\n\n    check_input : bool, default True\n        Skip input validation checks, including the Gram matrix when provided\n        assuming there are handled by the caller when check_input=False.\n\n    **params : kwargs\n        Keyword arguments passed to the coordinate descent solver.\n\n    Returns\n    -------\n    alphas : array, shape (n_alphas,)\n        The alphas along the path where models are computed.\n\n    coefs : array, shape (n_features, n_alphas) or             (n_outputs, n_features, n_alphas)\n        Coefficients along the path.\n\n    dual_gaps : array, shape (n_alphas,)\n        The dual gaps at the end of the optimization for each alpha.\n\n    n_iters : array-like, shape (n_alphas,)\n        The number of iterations taken by the coordinate descent optimizer to\n        reach the specified tolerance for each alpha.\n        (Is returned when ``return_n_iter`` is set to True).\n\n    See Also\n    --------\n    MultiTaskElasticNet\n    MultiTaskElasticNetCV\n    ElasticNet\n    ElasticNetCV\n\n    Notes\n    -----\n    For an example, see\n    :ref:`examples/linear_model/plot_lasso_coordinate_descent_path.py\n    <sphx_glr_auto_examples_linear_model_plot_lasso_coordinate_descent_path.py>`.\n    "
    if check_input:
        X = check_array(X, 'csc', dtype=[np.float64, np.float32], order='F', copy=copy_X)
        y = check_array(y, 'csc', dtype=X.dtype.type, order='F', copy=False, ensure_2d=False)
        if (Xy is not None):
            Xy = check_array(Xy, dtype=X.dtype.type, order='C', copy=False, ensure_2d=False)
    (n_samples, n_features) = X.shape
    multi_output = False
    if (y.ndim != 1):
        multi_output = True
        (_, n_outputs) = y.shape
    if (multi_output and positive):
        raise ValueError('positive=True is not allowed for multi-output (y.ndim != 1)')
    if ((not multi_output) and sparse.isspmatrix(X)):
        if ('X_offset' in params):
            X_sparse_scaling = (params['X_offset'] / params['X_scale'])
            X_sparse_scaling = np.asarray(X_sparse_scaling, dtype=X.dtype)
        else:
            X_sparse_scaling = np.zeros(n_features, dtype=X.dtype)
    if check_input:
        (X, y, X_offset, y_offset, X_scale, precompute, Xy) = _pre_fit(X, y, Xy, precompute, normalize=False, fit_intercept=False, copy=False, check_input=check_input)
    if (alphas is None):
        alphas = _alpha_grid(X, y, Xy=Xy, l1_ratio=l1_ratio, fit_intercept=False, eps=eps, n_alphas=n_alphas, normalize=False, copy_X=False)
    else:
        alphas = np.sort(alphas)[::(- 1)]
    n_alphas = len(alphas)
    tol = params.get('tol', 0.0001)
    max_iter = params.get('max_iter', 1000)
    dual_gaps = np.empty(n_alphas)
    n_iters = []
    rng = check_random_state(params.get('random_state', None))
    selection = params.get('selection', 'cyclic')
    if (selection not in ['random', 'cyclic']):
        raise ValueError('selection should be either random or cyclic.')
    random = (selection == 'random')
    if (not multi_output):
        coefs = np.empty((n_features, n_alphas), dtype=X.dtype)
    else:
        coefs = np.empty((n_outputs, n_features, n_alphas), dtype=X.dtype)
    if (coef_init is None):
        coef_ = np.zeros(coefs.shape[:(- 1)], dtype=X.dtype, order='F')
    else:
        coef_ = np.asfortranarray(coef_init, dtype=X.dtype)
    for (i, alpha) in enumerate(alphas):
        l1_reg = ((alpha * l1_ratio) * n_samples)
        l2_reg = ((alpha * (1.0 - l1_ratio)) * n_samples)
        if ((not multi_output) and sparse.isspmatrix(X)):
            model = cd_fast.sparse_enet_coordinate_descent(coef_, l1_reg, l2_reg, X.data, X.indices, X.indptr, y, X_sparse_scaling, max_iter, tol, rng, random, positive)
        elif multi_output:
            model = cd_fast.enet_coordinate_descent_multi_task(coef_, l1_reg, l2_reg, X, y, max_iter, tol, rng, random)
        elif isinstance(precompute, np.ndarray):
            if check_input:
                precompute = check_array(precompute, dtype=X.dtype.type, order='C')
            model = cd_fast.enet_coordinate_descent_gram(coef_, l1_reg, l2_reg, precompute, Xy, y, max_iter, tol, rng, random, positive)
        elif (precompute is False):
            model = cd_fast.enet_coordinate_descent(coef_, l1_reg, l2_reg, X, y, max_iter, tol, rng, random, positive)
        else:
            raise ValueError(("Precompute should be one of True, False, 'auto' or array-like. Got %r" % precompute))
        (coef_, dual_gap_, eps_, n_iter_) = model
        coefs[(..., i)] = coef_
        dual_gaps[i] = dual_gap_
        n_iters.append(n_iter_)
        if verbose:
            if (verbose > 2):
                print(model)
            elif (verbose > 1):
                print(('Path: %03i out of %03i' % (i, n_alphas)))
            else:
                sys.stderr.write('.')
    if return_n_iter:
        return (alphas, coefs, dual_gaps, n_iters)
    return (alphas, coefs, dual_gaps)