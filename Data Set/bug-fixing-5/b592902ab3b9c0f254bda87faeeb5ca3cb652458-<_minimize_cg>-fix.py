def _minimize_cg(fun, x0, args=(), jac=None, callback=None, gtol=1e-05, norm=Inf, eps=_epsilon, maxiter=None, disp=False, return_all=False, **unknown_options):
    '\n    Minimization of scalar function of one or more variables using the\n    conjugate gradient algorithm.\n\n    Options\n    -------\n    disp : bool\n        Set to True to print convergence messages.\n    maxiter : int\n        Maximum number of iterations to perform.\n    gtol : float\n        Gradient norm must be less than `gtol` before successful\n        termination.\n    norm : float\n        Order of norm (Inf is max, -Inf is min).\n    eps : float or ndarray\n        If `jac` is approximated, use this value for the step size.\n\n    '
    _check_unknown_options(unknown_options)
    f = fun
    fprime = jac
    epsilon = eps
    retall = return_all
    x0 = asarray(x0).flatten()
    if (maxiter is None):
        maxiter = (len(x0) * 200)
    (func_calls, f) = wrap_function(f, args)
    if (fprime is None):
        (grad_calls, myfprime) = wrap_function(approx_fprime, (f, epsilon))
    else:
        (grad_calls, myfprime) = wrap_function(fprime, args)
    gfk = myfprime(x0)
    k = 0
    xk = x0
    old_fval = f(xk)
    old_old_fval = (old_fval + (np.linalg.norm(gfk) / 2))
    if retall:
        allvecs = [xk]
    warnflag = 0
    pk = (- gfk)
    gnorm = vecnorm(gfk, ord=norm)
    sigma_3 = 0.01
    while ((gnorm > gtol) and (k < maxiter)):
        deltak = numpy.dot(gfk, gfk)
        cached_step = [None]

        def polak_ribiere_powell_step(alpha, gfkp1=None):
            xkp1 = (xk + (alpha * pk))
            if (gfkp1 is None):
                gfkp1 = myfprime(xkp1)
            yk = (gfkp1 - gfk)
            beta_k = max(0, (numpy.dot(yk, gfkp1) / deltak))
            pkp1 = ((- gfkp1) + (beta_k * pk))
            gnorm = vecnorm(gfkp1, ord=norm)
            return (alpha, xkp1, pkp1, gfkp1, gnorm)

        def descent_condition(alpha, xkp1, fp1, gfkp1):
            cached_step[:] = polak_ribiere_powell_step(alpha, gfkp1)
            (alpha, xk, pk, gfk, gnorm) = cached_step
            if (gnorm <= gtol):
                return True
            return (numpy.dot(pk, gfk) <= ((- sigma_3) * numpy.dot(gfk, gfk)))
        try:
            (alpha_k, fc, gc, old_fval, old_old_fval, gfkp1) = _line_search_wolfe12(f, myfprime, xk, pk, gfk, old_fval, old_old_fval, c2=0.4, amin=1e-100, amax=1e+100, extra_condition=descent_condition)
        except _LineSearchError:
            warnflag = 2
            break
        if (alpha_k == cached_step[0]):
            (alpha_k, xk, pk, gfk, gnorm) = cached_step
        else:
            (alpha_k, xk, pk, gfk, gnorm) = polak_ribiere_powell_step(alpha_k, gfkp1)
        if retall:
            allvecs.append(xk)
        if (callback is not None):
            callback(xk)
        k += 1
    fval = old_fval
    if (warnflag == 2):
        msg = _status_message['pr_loss']
    elif (k >= maxiter):
        warnflag = 1
        msg = _status_message['maxiter']
    else:
        msg = _status_message['success']
    if disp:
        print(('%s%s' % (('Warning: ' if (warnflag != 0) else ''), msg)))
        print(('         Current function value: %f' % fval))
        print(('         Iterations: %d' % k))
        print(('         Function evaluations: %d' % func_calls[0]))
        print(('         Gradient evaluations: %d' % grad_calls[0]))
    result = OptimizeResult(fun=fval, jac=gfk, nfev=func_calls[0], njev=grad_calls[0], status=warnflag, success=(warnflag == 0), message=msg, x=xk, nit=k)
    if retall:
        result['allvecs'] = allvecs
    return result