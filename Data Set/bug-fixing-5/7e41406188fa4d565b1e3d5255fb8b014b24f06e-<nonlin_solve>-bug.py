def nonlin_solve(F, x0, jacobian='krylov', iter=None, verbose=False, maxiter=None, f_tol=None, f_rtol=None, x_tol=None, x_rtol=None, tol_norm=None, line_search='armijo', callback=None, full_output=False, raise_exception=True):
    '\n    Find a root of a function, in a way suitable for large-scale problems.\n\n    Parameters\n    ----------\n    %(params_basic)s\n    jacobian : Jacobian\n        A Jacobian approximation: `Jacobian` object or something that\n        `asjacobian` can transform to one. Alternatively, a string specifying\n        which of the builtin Jacobian approximations to use:\n\n            krylov, broyden1, broyden2, anderson\n            diagbroyden, linearmixing, excitingmixing\n\n    %(params_extra)s\n    full_output : bool\n        If true, returns a dictionary `info` containing convergence\n        information.\n    raise_exception : bool\n        If True, a `NoConvergence` exception is raise if no solution is found.\n\n    See Also\n    --------\n    asjacobian, Jacobian\n\n    Notes\n    -----\n    This algorithm implements the inexact Newton method, with\n    backtracking or full line searches. Several Jacobian\n    approximations are available, including Krylov and Quasi-Newton\n    methods.\n\n    References\n    ----------\n    .. [KIM] C. T. Kelley, "Iterative Methods for Linear and Nonlinear\n       Equations". Society for Industrial and Applied Mathematics. (1995)\n       https://archive.siam.org/books/kelley/fr16/\n\n    '
    condition = TerminationCondition(f_tol=f_tol, f_rtol=f_rtol, x_tol=x_tol, x_rtol=x_rtol, iter=iter, norm=tol_norm)
    x0 = _as_inexact(x0)
    func = (lambda z: _as_inexact(F(_array_like(z, x0))).flatten())
    x = x0.flatten()
    dx = np.inf
    Fx = func(x)
    Fx_norm = norm(Fx)
    jacobian = asjacobian(jacobian)
    jacobian.setup(x.copy(), Fx, func)
    if (maxiter is None):
        if (iter is not None):
            maxiter = (iter + 1)
        else:
            maxiter = (100 * (x.size + 1))
    if (line_search is True):
        line_search = 'armijo'
    elif (line_search is False):
        line_search = None
    if (line_search not in (None, 'armijo', 'wolfe')):
        raise ValueError('Invalid line search')
    gamma = 0.9
    eta_max = 0.9999
    eta_treshold = 0.1
    eta = 0.001
    for n in xrange(maxiter):
        status = condition.check(Fx, x, dx)
        if status:
            break
        tol = min(eta, (eta * Fx_norm))
        dx = (- jacobian.solve(Fx, tol=tol))
        if (norm(dx) == 0):
            raise ValueError('Jacobian inversion yielded zero vector. This indicates a bug in the Jacobian approximation.')
        if line_search:
            (s, x, Fx, Fx_norm_new) = _nonlin_line_search(func, x, Fx, dx, line_search)
        else:
            s = 1.0
            x = (x + dx)
            Fx = func(x)
            Fx_norm_new = norm(Fx)
        jacobian.update(x.copy(), Fx)
        if callback:
            callback(x, Fx)
        eta_A = ((gamma * (Fx_norm_new ** 2)) / (Fx_norm ** 2))
        if ((gamma * (eta ** 2)) < eta_treshold):
            eta = min(eta_max, eta_A)
        else:
            eta = min(eta_max, max(eta_A, (gamma * (eta ** 2))))
        Fx_norm = Fx_norm_new
        if verbose:
            sys.stdout.write(('%d:  |F(x)| = %g; step %g; tol %g\n' % (n, norm(Fx), s, eta)))
            sys.stdout.flush()
    else:
        if raise_exception:
            raise NoConvergence(_array_like(x, x0))
        else:
            status = 2
    if full_output:
        info = {
            'nit': condition.iteration,
            'fun': Fx,
            'status': status,
            'success': (status == 1),
            'message': {
                1: 'A solution was found at the specified tolerance.',
                2: 'The maximum number of iterations allowed has been reached.',
            }[status],
        }
        return (_array_like(x, x0), info)
    else:
        return _array_like(x, x0)