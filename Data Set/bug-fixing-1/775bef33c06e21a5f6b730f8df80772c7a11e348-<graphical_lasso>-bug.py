

def graphical_lasso(emp_cov, alpha, cov_init=None, mode='cd', tol=0.0001, enet_tol=0.0001, max_iter=100, verbose=False, return_costs=False, eps=np.finfo(np.float64).eps, return_n_iter=False):
    "l1-penalized covariance estimator\n\n    Read more in the :ref:`User Guide <sparse_inverse_covariance>`.\n\n    Parameters\n    ----------\n    emp_cov : 2D ndarray, shape (n_features, n_features)\n        Empirical covariance from which to compute the covariance estimate.\n\n    alpha : positive float\n        The regularization parameter: the higher alpha, the more\n        regularization, the sparser the inverse covariance.\n\n    cov_init : 2D array (n_features, n_features), optional\n        The initial guess for the covariance.\n\n    mode : {'cd', 'lars'}\n        The Lasso solver to use: coordinate descent or LARS. Use LARS for\n        very sparse underlying graphs, where p > n. Elsewhere prefer cd\n        which is more numerically stable.\n\n    tol : positive float, optional\n        The tolerance to declare convergence: if the dual gap goes below\n        this value, iterations are stopped.\n\n    enet_tol : positive float, optional\n        The tolerance for the elastic net solver used to calculate the descent\n        direction. This parameter controls the accuracy of the search direction\n        for a given column update, not of the overall parameter estimate. Only\n        used for mode='cd'.\n\n    max_iter : integer, optional\n        The maximum number of iterations.\n\n    verbose : boolean, optional\n        If verbose is True, the objective function and dual gap are\n        printed at each iteration.\n\n    return_costs : boolean, optional\n        If return_costs is True, the objective function and dual gap\n        at each iteration are returned.\n\n    eps : float, optional\n        The machine-precision regularization in the computation of the\n        Cholesky diagonal factors. Increase this for very ill-conditioned\n        systems.\n\n    return_n_iter : bool, optional\n        Whether or not to return the number of iterations.\n\n    Returns\n    -------\n    covariance : 2D ndarray, shape (n_features, n_features)\n        The estimated covariance matrix.\n\n    precision : 2D ndarray, shape (n_features, n_features)\n        The estimated (sparse) precision matrix.\n\n    costs : list of (objective, dual_gap) pairs\n        The list of values of the objective function and the dual gap at\n        each iteration. Returned only if return_costs is True.\n\n    n_iter : int\n        Number of iterations. Returned only if `return_n_iter` is set to True.\n\n    See Also\n    --------\n    GraphicalLasso, GraphicalLassoCV\n\n    Notes\n    -----\n    The algorithm employed to solve this problem is the GLasso algorithm,\n    from the Friedman 2008 Biostatistics paper. It is the same algorithm\n    as in the R `glasso` package.\n\n    One possible difference with the `glasso` R package is that the\n    diagonal coefficients are not penalized.\n\n    "
    (_, n_features) = emp_cov.shape
    if (alpha == 0):
        if return_costs:
            precision_ = linalg.inv(emp_cov)
            cost = ((- 2.0) * log_likelihood(emp_cov, precision_))
            cost += (n_features * np.log((2 * np.pi)))
            d_gap = (np.sum((emp_cov * precision_)) - n_features)
            if return_n_iter:
                return (emp_cov, precision_, (cost, d_gap), 0)
            else:
                return (emp_cov, precision_, (cost, d_gap))
        elif return_n_iter:
            return (emp_cov, linalg.inv(emp_cov), 0)
        else:
            return (emp_cov, linalg.inv(emp_cov))
    if (cov_init is None):
        covariance_ = emp_cov.copy()
    else:
        covariance_ = cov_init.copy()
    covariance_ *= 0.95
    diagonal = emp_cov.flat[::(n_features + 1)]
    covariance_.flat[::(n_features + 1)] = diagonal
    precision_ = linalg.pinvh(covariance_)
    indices = np.arange(n_features)
    costs = list()
    if (mode == 'cd'):
        errors = dict(over='raise', invalid='ignore')
    else:
        errors = dict(invalid='raise')
    try:
        d_gap = np.inf
        sub_covariance = np.ascontiguousarray(covariance_[1:, 1:])
        for i in range(max_iter):
            for idx in range(n_features):
                if (idx > 0):
                    di = (idx - 1)
                    sub_covariance[di] = covariance_[di][(indices != idx)]
                    sub_covariance[:, di] = covariance_[:, di][(indices != idx)]
                else:
                    sub_covariance[:] = covariance_[1:, 1:]
                row = emp_cov[(idx, (indices != idx))]
                with np.errstate(**errors):
                    if (mode == 'cd'):
                        coefs = (- (precision_[((indices != idx), idx)] / (precision_[(idx, idx)] + (1000 * eps))))
                        (coefs, _, _, _) = cd_fast.enet_coordinate_descent_gram(coefs, alpha, 0, sub_covariance, row, row, max_iter, enet_tol, check_random_state(None), False)
                    else:
                        (_, _, coefs) = lars_path(sub_covariance, row, Xy=row, Gram=sub_covariance, alpha_min=(alpha / (n_features - 1)), copy_Gram=True, eps=eps, method='lars', return_path=False)
                precision_[(idx, idx)] = (1.0 / (covariance_[(idx, idx)] - np.dot(covariance_[((indices != idx), idx)], coefs)))
                precision_[((indices != idx), idx)] = ((- precision_[(idx, idx)]) * coefs)
                precision_[(idx, (indices != idx))] = ((- precision_[(idx, idx)]) * coefs)
                coefs = np.dot(sub_covariance, coefs)
                covariance_[(idx, (indices != idx))] = coefs
                covariance_[((indices != idx), idx)] = coefs
            d_gap = _dual_gap(emp_cov, precision_, alpha)
            cost = _objective(emp_cov, precision_, alpha)
            if verbose:
                print(('[graphical_lasso] Iteration % 3i, cost % 3.2e, dual gap %.3e' % (i, cost, d_gap)))
            if return_costs:
                costs.append((cost, d_gap))
            if (np.abs(d_gap) < tol):
                break
            if ((not np.isfinite(cost)) and (i > 0)):
                raise FloatingPointError('Non SPD result: the system is too ill-conditioned for this solver')
        else:
            warnings.warn(('graphical_lasso: did not converge after %i iteration: dual gap: %.3e' % (max_iter, d_gap)), ConvergenceWarning)
    except FloatingPointError as e:
        e.args = ((e.args[0] + '. The system is too ill-conditioned for this solver'),)
        raise e
    if return_costs:
        if return_n_iter:
            return (covariance_, precision_, costs, (i + 1))
        else:
            return (covariance_, precision_, costs)
    elif return_n_iter:
        return (covariance_, precision_, (i + 1))
    else:
        return (covariance_, precision_)
