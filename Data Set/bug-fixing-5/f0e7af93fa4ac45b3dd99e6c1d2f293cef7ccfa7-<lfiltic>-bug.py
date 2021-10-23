def lfiltic(b, a, y, x=None):
    '\n    Construct initial conditions for lfilter given input and output vectors.\n\n    Given a linear filter (b, a) and initial conditions on the output `y`\n    and the input `x`, return the initial conditions on the state vector zi\n    which is used by `lfilter` to generate the output given the input.\n\n    Parameters\n    ----------\n    b : array_like\n        Linear filter term.\n    a : array_like\n        Linear filter term.\n    y : array_like\n        Initial conditions.\n\n        If ``N = len(a) - 1``, then ``y = {y[-1], y[-2], ..., y[-N]}``.\n\n        If `y` is too short, it is padded with zeros.\n    x : array_like, optional\n        Initial conditions.\n\n        If ``M = len(b) - 1``, then ``x = {x[-1], x[-2], ..., x[-M]}``.\n\n        If `x` is not given, its initial conditions are assumed zero.\n\n        If `x` is too short, it is padded with zeros.\n\n    Returns\n    -------\n    zi : ndarray\n        The state vector ``zi = {z_0[-1], z_1[-1], ..., z_K-1[-1]}``,\n        where ``K = max(M, N)``.\n\n    See Also\n    --------\n    lfilter, lfilter_zi\n\n    '
    N = (np.size(a) - 1)
    M = (np.size(b) - 1)
    K = max(M, N)
    y = asarray(y)
    if (y.dtype.kind in 'bui'):
        y = y.astype(np.float64)
    zi = zeros(K, y.dtype)
    if (x is None):
        x = zeros(M, y.dtype)
    else:
        x = asarray(x)
        L = np.size(x)
        if (L < M):
            x = r_[(x, zeros((M - L)))]
    L = np.size(y)
    if (L < N):
        y = r_[(y, zeros((N - L)))]
    for m in range(M):
        zi[m] = np.sum((b[(m + 1):] * x[:(M - m)]), axis=0)
    for m in range(N):
        zi[m] -= np.sum((a[(m + 1):] * y[:(N - m)]), axis=0)
    return zi