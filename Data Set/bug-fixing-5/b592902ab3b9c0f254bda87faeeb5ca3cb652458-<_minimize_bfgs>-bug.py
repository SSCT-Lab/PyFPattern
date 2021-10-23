def _minimize_bfgs(fun, x0, args=(), jac=None, callback=None, gtol=1e-05, norm=Inf, eps=_epsilon, maxiter=None, disp=False, return_all=False, **unknown_options):
    '\n    Minimization of scalar function of one or more variables using the\n    BFGS algorithm.\n\n    Options\n    -------\n    disp : bool\n        Set to True to print convergence messages.\n    maxiter : int\n        Maximum number of iterations to perform.\n    gtol : float\n        Gradient norm must be less than `gtol` before successful\n        termination.\n    norm : float\n        Order of norm (Inf is max, -Inf is min).\n    eps : float or ndarray\n        If `jac` is approximated, use this value for the step size.\n\n    '
    _check_unknown_options(unknown_options)
    f = fun
    fprime = jac
    epsilon = eps
    retall = return_all
    x0 = asarray(x0).flatten()
    if (x0.ndim == 0):
        x0.shape = (1,)
    if (maxiter is None):
        maxiter = (len(x0) * 200)
    (func_calls, f) = wrap_function(f, args)
    if (fprime is None):
        (grad_calls, myfprime) = wrap_function(approx_fprime, (f, epsilon))
    else:
        (grad_calls, myfprime) = wrap_function(fprime, args)
    gfk = myfprime(x0)
    k = 0
    N = len(x0)
    I = numpy.eye(N, dtype=int)
    Hk = I
    old_fval = f(x0)
    old_old_fval = (old_fval + (np.linalg.norm(gfk) / 2))
    xk = x0
    if retall:
        allvecs = [x0]
    sk = [(2 * gtol)]
    warnflag = 0
    gnorm = vecnorm(gfk, ord=norm)
    while ((gnorm > gtol) and (k < maxiter)):
        pk = (- numpy.dot(Hk, gfk))
        try:
            (alpha_k, fc, gc, old_fval, old_old_fval, gfkp1) = _line_search_wolfe12(f, myfprime, xk, pk, gfk, old_fval, old_old_fval, amin=1e-100, amax=1e+100)
        except _LineSearchError:
            warnflag = 2
            break
        xkp1 = (xk + (alpha_k * pk))
        if retall:
            allvecs.append(xkp1)
        sk = (xkp1 - xk)
        xk = xkp1
        if (gfkp1 is None):
            gfkp1 = myfprime(xkp1)
        yk = (gfkp1 - gfk)
        gfk = gfkp1
        if (callback is not None):
            callback(xk)
        k += 1
        gnorm = vecnorm(gfk, ord=norm)
        if (gnorm <= gtol):
            break
        if (not numpy.isfinite(old_fval)):
            warnflag = 2
            break
        try:
            rhok = (1.0 / numpy.dot(yk, sk))
        except ZeroDivisionError:
            rhok = 1000.0
            if disp:
                print('Divide-by-zero encountered: rhok assumed large')
        if isinf(rhok):
            rhok = 1000.0
            if disp:
                print('Divide-by-zero encountered: rhok assumed large')
        A1 = (I - ((sk[:, numpy.newaxis] * yk[numpy.newaxis, :]) * rhok))
        A2 = (I - ((yk[:, numpy.newaxis] * sk[numpy.newaxis, :]) * rhok))
        Hk = (numpy.dot(A1, numpy.dot(Hk, A2)) + ((rhok * sk[:, numpy.newaxis]) * sk[numpy.newaxis, :]))
    fval = old_fval
    if np.isnan(fval):
        warnflag = 2
    if (warnflag == 2):
        msg = _status_message['pr_loss']
        if disp:
            print(('Warning: ' + msg))
            print(('         Current function value: %f' % fval))
            print(('         Iterations: %d' % k))
            print(('         Function evaluations: %d' % func_calls[0]))
            print(('         Gradient evaluations: %d' % grad_calls[0]))
    elif (k >= maxiter):
        warnflag = 1
        msg = _status_message['maxiter']
        if disp:
            print(('Warning: ' + msg))
            print(('         Current function value: %f' % fval))
            print(('         Iterations: %d' % k))
            print(('         Function evaluations: %d' % func_calls[0]))
            print(('         Gradient evaluations: %d' % grad_calls[0]))
    else:
        msg = _status_message['success']
        if disp:
            print(msg)
            print(('         Current function value: %f' % fval))
            print(('         Iterations: %d' % k))
            print(('         Function evaluations: %d' % func_calls[0]))
            print(('         Gradient evaluations: %d' % grad_calls[0]))
    result = OptimizeResult(fun=fval, jac=gfk, hess_inv=Hk, nfev=func_calls[0], njev=grad_calls[0], status=warnflag, success=(warnflag == 0), message=msg, x=xk, nit=k)
    if retall:
        result['allvecs'] = allvecs
    return result