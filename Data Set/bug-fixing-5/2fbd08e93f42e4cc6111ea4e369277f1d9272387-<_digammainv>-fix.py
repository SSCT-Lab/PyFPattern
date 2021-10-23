def _digammainv(y):
    _em = 0.5772156649015329
    func = (lambda x: (sc.digamma(x) - y))
    if (y > (- 0.125)):
        x0 = (np.exp(y) + 0.5)
        if (y < 10):
            value = optimize.newton(func, x0, tol=1e-10)
            return value
    elif (y > (- 3)):
        x0 = (np.exp((y / 2.332)) + 0.08661)
    else:
        x0 = (1.0 / ((- y) - _em))
    (value, info, ier, mesg) = optimize.fsolve(func, x0, xtol=1e-11, full_output=True)
    if (ier != 1):
        raise RuntimeError(('_digammainv: fsolve failed, y = %r' % y))
    return value[0]