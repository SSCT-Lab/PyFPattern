def lars_path(X, y, Xy=None, Gram=None, max_iter=500, alpha_min=0, method='lar', copy_X=True, eps=np.finfo(np.float).eps, copy_Gram=True, verbose=0, return_path=True, return_n_iter=False, positive=False):
    'Compute Least Angle Regression or Lasso path using LARS algorithm [1]\n\n    The optimization objective for the case method=\'lasso\' is::\n\n    (1 / (2 * n_samples)) * ||y - Xw||^2_2 + alpha * ||w||_1\n\n    in the case of method=\'lars\', the objective function is only known in\n    the form of an implicit equation (see discussion in [1])\n\n    Read more in the :ref:`User Guide <least_angle_regression>`.\n\n    Parameters\n    -----------\n    X : array, shape: (n_samples, n_features)\n        Input data.\n\n    y : array, shape: (n_samples)\n        Input targets.\n\n    positive : boolean (default=False)\n        Restrict coefficients to be >= 0.\n        When using this option together with method \'lasso\' the model\n        coefficients will not converge to the ordinary-least-squares solution\n        for small values of alpha (neither will they when using method \'lar\'\n        ..). Only coeffiencts up to the smallest alpha value (``alphas_[alphas_ >\n        0.].min()`` when fit_path=True) reached by the stepwise Lars-Lasso\n        algorithm are typically in congruence with the solution of the\n        coordinate descent lasso_path function.\n\n    max_iter : integer, optional (default=500)\n        Maximum number of iterations to perform, set to infinity for no limit.\n\n    Gram : None, \'auto\', array, shape: (n_features, n_features), optional\n        Precomputed Gram matrix (X\' * X), if ``\'auto\'``, the Gram\n        matrix is precomputed from the given X, if there are more samples\n        than features.\n\n    alpha_min : float, optional (default=0)\n        Minimum correlation along the path. It corresponds to the\n        regularization parameter alpha parameter in the Lasso.\n\n    method : {\'lar\', \'lasso\'}, optional (default=\'lar\')\n        Specifies the returned model. Select ``\'lar\'`` for Least Angle\n        Regression, ``\'lasso\'`` for the Lasso.\n\n    eps : float, optional (default=``np.finfo(np.float).eps``)\n        The machine-precision regularization in the computation of the\n        Cholesky diagonal factors. Increase this for very ill-conditioned\n        systems.\n\n    copy_X : bool, optional (default=True)\n        If ``False``, ``X`` is overwritten.\n\n    copy_Gram : bool, optional (default=True)\n        If ``False``, ``Gram`` is overwritten.\n\n    verbose : int (default=0)\n        Controls output verbosity.\n\n    return_path : bool, optional (default=True)\n        If ``return_path==True`` returns the entire path, else returns only the\n        last point of the path.\n\n    return_n_iter : bool, optional (default=False)\n        Whether to return the number of iterations.\n\n    Returns\n    --------\n    alphas : array, shape: [n_alphas + 1]\n        Maximum of covariances (in absolute value) at each iteration.\n        ``n_alphas`` is either ``max_iter``, ``n_features`` or the\n        number of nodes in the path with ``alpha >= alpha_min``, whichever\n        is smaller.\n\n    active : array, shape [n_alphas]\n        Indices of active variables at the end of the path.\n\n    coefs : array, shape (n_features, n_alphas + 1)\n        Coefficients along the path\n\n    n_iter : int\n        Number of iterations run. Returned only if return_n_iter is set\n        to True.\n\n    See also\n    --------\n    lasso_path\n    LassoLars\n    Lars\n    LassoLarsCV\n    LarsCV\n    sklearn.decomposition.sparse_encode\n\n    References\n    ----------\n    .. [1] "Least Angle Regression", Effron et al.\n           http://statweb.stanford.edu/~tibs/ftp/lars.pdf\n\n    .. [2] `Wikipedia entry on the Least-angle regression\n           <https://en.wikipedia.org/wiki/Least-angle_regression>`_\n\n    .. [3] `Wikipedia entry on the Lasso\n           <https://en.wikipedia.org/wiki/Lasso_(statistics)#Lasso_method>`_\n\n    '
    n_features = X.shape[1]
    n_samples = y.size
    max_features = min(max_iter, n_features)
    if return_path:
        coefs = np.zeros(((max_features + 1), n_features))
        alphas = np.zeros((max_features + 1))
    else:
        (coef, prev_coef) = (np.zeros(n_features), np.zeros(n_features))
        (alpha, prev_alpha) = (np.array([0.0]), np.array([0.0]))
    (n_iter, n_active) = (0, 0)
    (active, indices) = (list(), np.arange(n_features))
    sign_active = np.empty(max_features, dtype=np.int8)
    drop = False
    L = np.zeros((max_features, max_features), dtype=X.dtype)
    (swap, nrm2) = linalg.get_blas_funcs(('swap', 'nrm2'), (X,))
    (solve_cholesky,) = get_lapack_funcs(('potrs',), (X,))
    if (Gram is None):
        if copy_X:
            X = X.copy('F')
    elif (isinstance(Gram, string_types) and (Gram == 'auto')):
        Gram = None
        if (X.shape[0] > X.shape[1]):
            Gram = np.dot(X.T, X)
    elif copy_Gram:
        Gram = Gram.copy()
    if (Xy is None):
        Cov = np.dot(X.T, y)
    else:
        Cov = Xy.copy()
    if verbose:
        if (verbose > 1):
            print('Step\t\tAdded\t\tDropped\t\tActive set size\t\tC')
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
    tiny = np.finfo(np.float).tiny
    tiny32 = np.finfo(np.float32).tiny
    equality_tolerance = np.finfo(np.float32).eps
    while True:
        if Cov.size:
            if positive:
                C_idx = np.argmax(Cov)
            else:
                C_idx = np.argmax(np.abs(Cov))
            C_ = Cov[C_idx]
            if positive:
                C = C_
            else:
                C = np.fabs(C_)
        else:
            C = 0.0
        if return_path:
            alpha = alphas[(n_iter, np.newaxis)]
            coef = coefs[n_iter]
            prev_alpha = alphas[((n_iter - 1), np.newaxis)]
            prev_coef = coefs[(n_iter - 1)]
        alpha[0] = (C / n_samples)
        if (alpha[0] <= (alpha_min + equality_tolerance)):
            if (abs((alpha[0] - alpha_min)) > equality_tolerance):
                if (n_iter > 0):
                    ss = ((prev_alpha[0] - alpha_min) / (prev_alpha[0] - alpha[0]))
                    coef[:] = (prev_coef + (ss * (coef - prev_coef)))
                alpha[0] = alpha_min
            if return_path:
                coefs[n_iter] = coef
            break
        if ((n_iter >= max_iter) or (n_active >= n_features)):
            break
        if (not drop):
            if positive:
                sign_active[n_active] = np.ones_like(C_)
            else:
                sign_active[n_active] = np.sign(C_)
            (m, n) = (n_active, (C_idx + n_active))
            (Cov[C_idx], Cov[0]) = swap(Cov[C_idx], Cov[0])
            (indices[n], indices[m]) = (indices[m], indices[n])
            Cov_not_shortened = Cov
            Cov = Cov[1:]
            if (Gram is None):
                (X.T[n], X.T[m]) = swap(X.T[n], X.T[m])
                c = (nrm2(X.T[n_active]) ** 2)
                L[n_active, :n_active] = np.dot(X.T[n_active], X.T[:n_active].T)
            else:
                (Gram[m], Gram[n]) = swap(Gram[m], Gram[n])
                (Gram[:, m], Gram[:, n]) = swap(Gram[:, m], Gram[:, n])
                c = Gram[(n_active, n_active)]
                L[n_active, :n_active] = Gram[n_active, :n_active]
            if n_active:
                linalg.solve_triangular(L[:n_active, :n_active], L[n_active, :n_active], trans=0, lower=1, overwrite_b=True, **solve_triangular_args)
            v = np.dot(L[n_active, :n_active], L[n_active, :n_active])
            diag = max(np.sqrt(np.abs((c - v))), eps)
            L[(n_active, n_active)] = diag
            if (diag < 1e-07):
                warnings.warn(('Regressors in active set degenerate. Dropping a regressor, after %i iterations, i.e. alpha=%.3e, with an active set of %i regressors, and the smallest cholesky pivot element being %.3e' % (n_iter, alpha, n_active, diag)), ConvergenceWarning)
                Cov = Cov_not_shortened
                Cov[0] = 0
                (Cov[C_idx], Cov[0]) = swap(Cov[C_idx], Cov[0])
                continue
            active.append(indices[n_active])
            n_active += 1
            if (verbose > 1):
                print(('%s\t\t%s\t\t%s\t\t%s\t\t%s' % (n_iter, active[(- 1)], '', n_active, C)))
        if ((method == 'lasso') and (n_iter > 0) and (prev_alpha[0] < alpha[0])):
            warnings.warn(('Early stopping the lars path, as the residues are small and the current value of alpha is no longer well controlled. %i iterations, alpha=%.3e, previous alpha=%.3e, with an active set of %i regressors.' % (n_iter, alpha, prev_alpha, n_active)), ConvergenceWarning)
            break
        (least_squares, info) = solve_cholesky(L[:n_active, :n_active], sign_active[:n_active], lower=True)
        if ((least_squares.size == 1) and (least_squares == 0)):
            least_squares[...] = 1
            AA = 1.0
        else:
            AA = (1.0 / np.sqrt(np.sum((least_squares * sign_active[:n_active]))))
            if (not np.isfinite(AA)):
                i = 0
                L_ = L[:n_active, :n_active].copy()
                while (not np.isfinite(AA)):
                    L_.flat[::(n_active + 1)] += ((2 ** i) * eps)
                    (least_squares, info) = solve_cholesky(L_, sign_active[:n_active], lower=True)
                    tmp = max(np.sum((least_squares * sign_active[:n_active])), eps)
                    AA = (1.0 / np.sqrt(tmp))
                    i += 1
            least_squares *= AA
        if (Gram is None):
            eq_dir = np.dot(X.T[:n_active].T, least_squares)
            corr_eq_dir = np.dot(X.T[n_active:], eq_dir)
        else:
            corr_eq_dir = np.dot(Gram[:n_active, n_active:].T, least_squares)
        g1 = arrayfuncs.min_pos(((C - Cov) / ((AA - corr_eq_dir) + tiny)))
        if positive:
            gamma_ = min(g1, (C / AA))
        else:
            g2 = arrayfuncs.min_pos(((C + Cov) / ((AA + corr_eq_dir) + tiny)))
            gamma_ = min(g1, g2, (C / AA))
        drop = False
        z = ((- coef[active]) / (least_squares + tiny32))
        z_pos = arrayfuncs.min_pos(z)
        if (z_pos < gamma_):
            idx = np.where((z == z_pos))[0][::(- 1)]
            sign_active[idx] = (- sign_active[idx])
            if (method == 'lasso'):
                gamma_ = z_pos
            drop = True
        n_iter += 1
        if return_path:
            if (n_iter >= coefs.shape[0]):
                del coef, alpha, prev_alpha, prev_coef
                add_features = (2 * max(1, (max_features - n_active)))
                coefs = np.resize(coefs, ((n_iter + add_features), n_features))
                alphas = np.resize(alphas, (n_iter + add_features))
            coef = coefs[n_iter]
            prev_coef = coefs[(n_iter - 1)]
            alpha = alphas[(n_iter, np.newaxis)]
            prev_alpha = alphas[((n_iter - 1), np.newaxis)]
        else:
            prev_coef = coef
            prev_alpha[0] = alpha[0]
            coef = np.zeros_like(coef)
        coef[active] = (prev_coef[active] + (gamma_ * least_squares))
        Cov -= (gamma_ * corr_eq_dir)
        if (drop and (method == 'lasso')):
            [arrayfuncs.cholesky_delete(L[:n_active, :n_active], ii) for ii in idx]
            n_active -= 1
            (m, n) = (idx, n_active)
            drop_idx = [active.pop(ii) for ii in idx]
            if (Gram is None):
                for ii in idx:
                    for i in range(ii, n_active):
                        (X.T[i], X.T[(i + 1)]) = swap(X.T[i], X.T[(i + 1)])
                        (indices[i], indices[(i + 1)]) = (indices[(i + 1)], indices[i])
                residual = (y - np.dot(X[:, :n_active], coef[active]))
                temp = np.dot(X.T[n_active], residual)
                Cov = np.r_[(temp, Cov)]
            else:
                for ii in idx:
                    for i in range(ii, n_active):
                        (indices[i], indices[(i + 1)]) = (indices[(i + 1)], indices[i])
                        (Gram[i], Gram[(i + 1)]) = swap(Gram[i], Gram[(i + 1)])
                        (Gram[:, i], Gram[:, (i + 1)]) = swap(Gram[:, i], Gram[:, (i + 1)])
                residual = (y - np.dot(X, coef))
                temp = np.dot(X.T[drop_idx], residual)
                Cov = np.r_[(temp, Cov)]
            sign_active = np.delete(sign_active, idx)
            sign_active = np.append(sign_active, 0.0)
            if (verbose > 1):
                print(('%s\t\t%s\t\t%s\t\t%s\t\t%s' % (n_iter, '', drop_idx, n_active, abs(temp))))
    if return_path:
        alphas = alphas[:(n_iter + 1)]
        coefs = coefs[:(n_iter + 1)]
        if return_n_iter:
            return (alphas, active, coefs.T, n_iter)
        else:
            return (alphas, active, coefs.T)
    elif return_n_iter:
        return (alpha, active, coef, n_iter)
    else:
        return (alpha, active, coef)