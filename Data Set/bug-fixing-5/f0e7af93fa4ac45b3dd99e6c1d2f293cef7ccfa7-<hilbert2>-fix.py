def hilbert2(x, N=None):
    '\n    Compute the \'2-D\' analytic signal of `x`\n\n    Parameters\n    ----------\n    x : array_like\n        2-D signal data.\n    N : int or tuple of two ints, optional\n        Number of Fourier components. Default is ``x.shape``\n\n    Returns\n    -------\n    xa : ndarray\n        Analytic signal of `x` taken along axes (0,1).\n\n    References\n    ----------\n    .. [1] Wikipedia, "Analytic signal",\n        https://en.wikipedia.org/wiki/Analytic_signal\n\n    '
    x = np.atleast_2d(x)
    if (x.ndim > 2):
        raise ValueError('x must be 2-D.')
    if np.iscomplexobj(x):
        raise ValueError('x must be real.')
    if (N is None):
        N = x.shape
    elif isinstance(N, int):
        if (N <= 0):
            raise ValueError('N must be positive.')
        N = (N, N)
    elif ((len(N) != 2) or np.any((np.asarray(N) <= 0))):
        raise ValueError('When given as a tuple, N must hold exactly two positive integers')
    Xf = sp_fft.fft2(x, N, axes=(0, 1))
    h1 = np.zeros(N[0], 'd')
    h2 = np.zeros(N[1], 'd')
    for p in range(2):
        h = eval(('h%d' % (p + 1)))
        N1 = N[p]
        if ((N1 % 2) == 0):
            h[0] = h[(N1 // 2)] = 1
            h[1:(N1 // 2)] = 2
        else:
            h[0] = 1
            h[1:((N1 + 1) // 2)] = 2
        exec(('h%d = h' % (p + 1)), globals(), locals())
    h = (h1[:, np.newaxis] * h2[np.newaxis, :])
    k = x.ndim
    while (k > 2):
        h = h[:, np.newaxis]
        k -= 1
    x = sp_fft.ifft2((Xf * h), axes=(0, 1))
    return x