def romb(y, dx=1.0, axis=(- 1), show=False):
    '\n    Romberg integration using samples of a function.\n\n    Parameters\n    ----------\n    y : array_like\n        A vector of ``2**k + 1`` equally-spaced samples of a function.\n    dx : float, optional\n        The sample spacing. Default is 1.\n    axis : int, optional\n        The axis along which to integrate. Default is -1 (last axis).\n    show : bool, optional\n        When `y` is a single 1-D array, then if this argument is True\n        print the table showing Richardson extrapolation from the\n        samples. Default is False.\n\n    Returns\n    -------\n    romb : ndarray\n        The integrated result for `axis`.\n\n    See also\n    --------\n    quad : adaptive quadrature using QUADPACK\n    romberg : adaptive Romberg quadrature\n    quadrature : adaptive Gaussian quadrature\n    fixed_quad : fixed-order Gaussian quadrature\n    dblquad : double integrals\n    tplquad : triple integrals\n    simps : integrators for sampled data\n    cumtrapz : cumulative integration for sampled data\n    ode : ODE integrators\n    odeint : ODE integrators\n\n    '
    y = np.asarray(y)
    nd = len(y.shape)
    Nsamps = y.shape[axis]
    Ninterv = (Nsamps - 1)
    n = 1
    k = 0
    while (n < Ninterv):
        n <<= 1
        k += 1
    if (n != Ninterv):
        raise ValueError('Number of samples must be one plus a non-negative power of 2.')
    R = {
        
    }
    slice_all = ((slice(None),) * nd)
    slice0 = tupleset(slice_all, axis, 0)
    slicem1 = tupleset(slice_all, axis, (- 1))
    h = (Ninterv * np.asarray(dx, dtype=float))
    R[(0, 0)] = (((y[slice0] + y[slicem1]) / 2.0) * h)
    slice_R = slice_all
    start = stop = step = Ninterv
    for i in xrange(1, (k + 1)):
        start >>= 1
        slice_R = tupleset(slice_R, axis, slice(start, stop, step))
        step >>= 1
        R[(i, 0)] = (0.5 * (R[((i - 1), 0)] + (h * y[slice_R].sum(axis=axis))))
        for j in xrange(1, (i + 1)):
            prev = R[(i, (j - 1))]
            R[(i, j)] = (prev + ((prev - R[((i - 1), (j - 1))]) / ((1 << (2 * j)) - 1)))
        h /= 2.0
    if show:
        if (not np.isscalar(R[(0, 0)])):
            print(('*** Printing table only supported for integrals' + ' of a single data set.'))
        else:
            try:
                precis = show[0]
            except (TypeError, IndexError):
                precis = 5
            try:
                width = show[1]
            except (TypeError, IndexError):
                width = 8
            formstr = ('%%%d.%df' % (width, precis))
            title = 'Richardson Extrapolation Table for Romberg Integration'
            print('', title.center(68), ('=' * 68), sep='\n', end='\n')
            for i in xrange((k + 1)):
                for j in xrange((i + 1)):
                    print((formstr % R[(i, j)]), end=' ')
                print()
            print(('=' * 68))
            print()
    return R[(k, k)]