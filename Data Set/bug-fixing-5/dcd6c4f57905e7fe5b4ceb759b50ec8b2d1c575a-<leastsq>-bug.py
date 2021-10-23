def leastsq(func, x0, args=(), Dfun=None, full_output=0, col_deriv=0, ftol=1.49012e-08, xtol=1.49012e-08, gtol=0.0, maxfev=0, epsfcn=None, factor=100, diag=None):
    '\n    Minimize the sum of squares of a set of equations.\n\n    ::\n\n        x = arg min(sum(func(y)**2,axis=0))\n                 y\n\n    Parameters\n    ----------\n    func : callable\n        should take at least one (possibly length N vector) argument and\n        returns M floating point numbers. It must not return NaNs or\n        fitting might fail.\n    x0 : ndarray\n        The starting estimate for the minimization.\n    args : tuple, optional\n        Any extra arguments to func are placed in this tuple.\n    Dfun : callable, optional\n        A function or method to compute the Jacobian of func with derivatives\n        across the rows. If this is None, the Jacobian will be estimated.\n    full_output : bool, optional\n        non-zero to return all optional outputs.\n    col_deriv : bool, optional\n        non-zero to specify that the Jacobian function computes derivatives\n        down the columns (faster, because there is no transpose operation).\n    ftol : float, optional\n        Relative error desired in the sum of squares.\n    xtol : float, optional\n        Relative error desired in the approximate solution.\n    gtol : float, optional\n        Orthogonality desired between the function vector and the columns of\n        the Jacobian.\n    maxfev : int, optional\n        The maximum number of calls to the function. If `Dfun` is provided\n        then the default `maxfev` is 100*(N+1) where N is the number of elements\n        in x0, otherwise the default `maxfev` is 200*(N+1).\n    epsfcn : float, optional\n        A variable used in determining a suitable step length for the forward-\n        difference approximation of the Jacobian (for Dfun=None).\n        Normally the actual step length will be sqrt(epsfcn)*x\n        If epsfcn is less than the machine precision, it is assumed that the\n        relative errors are of the order of the machine precision.\n    factor : float, optional\n        A parameter determining the initial step bound\n        (``factor * || diag * x||``). Should be in interval ``(0.1, 100)``.\n    diag : sequence, optional\n        N positive entries that serve as a scale factors for the variables.\n\n    Returns\n    -------\n    x : ndarray\n        The solution (or the result of the last iteration for an unsuccessful\n        call).\n    cov_x : ndarray\n        Uses the fjac and ipvt optional outputs to construct an\n        estimate of the jacobian around the solution. None if a\n        singular matrix encountered (indicates very flat curvature in\n        some direction).  This matrix must be multiplied by the\n        residual variance to get the covariance of the\n        parameter estimates -- see curve_fit.\n    infodict : dict\n        a dictionary of optional outputs with the key s:\n\n        ``nfev``\n            The number of function calls\n        ``fvec``\n            The function evaluated at the output\n        ``fjac``\n            A permutation of the R matrix of a QR\n            factorization of the final approximate\n            Jacobian matrix, stored column wise.\n            Together with ipvt, the covariance of the\n            estimate can be approximated.\n        ``ipvt``\n            An integer array of length N which defines\n            a permutation matrix, p, such that\n            fjac*p = q*r, where r is upper triangular\n            with diagonal elements of nonincreasing\n            magnitude. Column j of p is column ipvt(j)\n            of the identity matrix.\n        ``qtf``\n            The vector (transpose(q) * fvec).\n\n    mesg : str\n        A string message giving information about the cause of failure.\n    ier : int\n        An integer flag.  If it is equal to 1, 2, 3 or 4, the solution was\n        found.  Otherwise, the solution was not found. In either case, the\n        optional output variable \'mesg\' gives more information.\n\n    Notes\n    -----\n    "leastsq" is a wrapper around MINPACK\'s lmdif and lmder algorithms.\n\n    cov_x is a Jacobian approximation to the Hessian of the least squares\n    objective function.\n    This approximation assumes that the objective function is based on the\n    difference between some observed target data (ydata) and a (non-linear)\n    function of the parameters `f(xdata, params)` ::\n\n           func(params) = ydata - f(xdata, params)\n\n    so that the objective function is ::\n\n           min   sum((ydata - f(xdata, params))**2, axis=0)\n         params\n\n    '
    x0 = asarray(x0).flatten()
    n = len(x0)
    if (not isinstance(args, tuple)):
        args = (args,)
    (shape, dtype) = _check_func('leastsq', 'func', func, x0, args, n)
    m = shape[0]
    if (n > m):
        raise TypeError(('Improper input: N=%s must not exceed M=%s' % (n, m)))
    if (epsfcn is None):
        epsfcn = finfo(dtype).eps
    if (Dfun is None):
        if (maxfev == 0):
            maxfev = (200 * (n + 1))
        with _MINPACK_LOCK:
            retval = _minpack._lmdif(func, x0, args, full_output, ftol, xtol, gtol, maxfev, epsfcn, factor, diag)
    else:
        if col_deriv:
            _check_func('leastsq', 'Dfun', Dfun, x0, args, n, (n, m))
        else:
            _check_func('leastsq', 'Dfun', Dfun, x0, args, n, (m, n))
        if (maxfev == 0):
            maxfev = (100 * (n + 1))
        with _MINPACK_LOCK:
            retval = _minpack._lmder(func, Dfun, x0, args, full_output, col_deriv, ftol, xtol, gtol, maxfev, factor, diag)
    errors = {
        0: ['Improper input parameters.', TypeError],
        1: [('Both actual and predicted relative reductions in the sum of squares\n  are at most %f' % ftol), None],
        2: [('The relative error between two consecutive iterates is at most %f' % xtol), None],
        3: [('Both actual and predicted relative reductions in the sum of squares\n  are at most %f and the relative error between two consecutive iterates is at \n  most %f' % (ftol, xtol)), None],
        4: [('The cosine of the angle between func(x) and any column of the\n  Jacobian is at most %f in absolute value' % gtol), None],
        5: [('Number of calls to function has reached maxfev = %d.' % maxfev), ValueError],
        6: [('ftol=%f is too small, no further reduction in the sum of squares\n  is possible.' % ftol), ValueError],
        7: [('xtol=%f is too small, no further improvement in the approximate\n  solution is possible.' % xtol), ValueError],
        8: [('gtol=%f is too small, func(x) is orthogonal to the columns of\n  the Jacobian to machine precision.' % gtol), ValueError],
        'unknown': ['Unknown error.', TypeError],
    }
    info = retval[(- 1)]
    if ((info not in [1, 2, 3, 4]) and (not full_output)):
        if (info in [5, 6, 7, 8]):
            warnings.warn(errors[info][0], RuntimeWarning)
        else:
            try:
                raise errors[info][1](errors[info][0])
            except KeyError:
                raise errors['unknown'][1](errors['unknown'][0])
    mesg = errors[info][0]
    if full_output:
        cov_x = None
        if (info in [1, 2, 3, 4]):
            from numpy.dual import inv
            perm = take(eye(n), (retval[1]['ipvt'] - 1), 0)
            r = triu(transpose(retval[1]['fjac'])[:n, :])
            R = dot(r, perm)
            try:
                cov_x = inv(dot(transpose(R), R))
            except (LinAlgError, ValueError):
                pass
        return (((retval[0], cov_x) + retval[1:(- 1)]) + (mesg, info))
    else:
        return (retval[0], info)