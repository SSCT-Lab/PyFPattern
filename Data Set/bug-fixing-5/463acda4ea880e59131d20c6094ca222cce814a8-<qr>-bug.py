@array_function_dispatch(_qr_dispatcher)
def qr(a, mode='reduced'):
    "\n    Compute the qr factorization of a matrix.\n\n    Factor the matrix `a` as *qr*, where `q` is orthonormal and `r` is\n    upper-triangular.\n\n    Parameters\n    ----------\n    a : array_like, shape (M, N)\n        Matrix to be factored.\n    mode : {'reduced', 'complete', 'r', 'raw'}, optional\n        If K = min(M, N), then\n\n        * 'reduced'  : returns q, r with dimensions (M, K), (K, N) (default)\n        * 'complete' : returns q, r with dimensions (M, M), (M, N)\n        * 'r'        : returns r only with dimensions (K, N)\n        * 'raw'      : returns h, tau with dimensions (N, M), (K,)\n\n        The options 'reduced', 'complete, and 'raw' are new in numpy 1.8,\n        see the notes for more information. The default is 'reduced', and to\n        maintain backward compatibility with earlier versions of numpy both\n        it and the old default 'full' can be omitted. Note that array h\n        returned in 'raw' mode is transposed for calling Fortran. The\n        'economic' mode is deprecated.  The modes 'full' and 'economic' may\n        be passed using only the first letter for backwards compatibility,\n        but all others must be spelled out. See the Notes for more\n        explanation.\n\n\n    Returns\n    -------\n    q : ndarray of float or complex, optional\n        A matrix with orthonormal columns. When mode = 'complete' the\n        result is an orthogonal/unitary matrix depending on whether or not\n        a is real/complex. The determinant may be either +/- 1 in that\n        case.\n    r : ndarray of float or complex, optional\n        The upper-triangular matrix.\n    (h, tau) : ndarrays of np.double or np.cdouble, optional\n        The array h contains the Householder reflectors that generate q\n        along with r. The tau array contains scaling factors for the\n        reflectors. In the deprecated  'economic' mode only h is returned.\n\n    Raises\n    ------\n    LinAlgError\n        If factoring fails.\n\n    Notes\n    -----\n    This is an interface to the LAPACK routines ``dgeqrf``, ``zgeqrf``,\n    ``dorgqr``, and ``zungqr``.\n\n    For more information on the qr factorization, see for example:\n    https://en.wikipedia.org/wiki/QR_factorization\n\n    Subclasses of `ndarray` are preserved except for the 'raw' mode. So if\n    `a` is of type `matrix`, all the return values will be matrices too.\n\n    New 'reduced', 'complete', and 'raw' options for mode were added in\n    NumPy 1.8.0 and the old option 'full' was made an alias of 'reduced'.  In\n    addition the options 'full' and 'economic' were deprecated.  Because\n    'full' was the previous default and 'reduced' is the new default,\n    backward compatibility can be maintained by letting `mode` default.\n    The 'raw' option was added so that LAPACK routines that can multiply\n    arrays by q using the Householder reflectors can be used. Note that in\n    this case the returned arrays are of type np.double or np.cdouble and\n    the h array is transposed to be FORTRAN compatible.  No routines using\n    the 'raw' return are currently exposed by numpy, but some are available\n    in lapack_lite and just await the necessary work.\n\n    Examples\n    --------\n    >>> a = np.random.randn(9, 6)\n    >>> q, r = np.linalg.qr(a)\n    >>> np.allclose(a, np.dot(q, r))  # a does equal qr\n    True\n    >>> r2 = np.linalg.qr(a, mode='r')\n    >>> np.allclose(r, r2)  # mode='r' returns the same r as mode='full'\n    True\n\n    Example illustrating a common use of `qr`: solving of least squares\n    problems\n\n    What are the least-squares-best `m` and `y0` in ``y = y0 + mx`` for\n    the following data: {(0,1), (1,0), (1,2), (2,1)}. (Graph the points\n    and you'll see that it should be y0 = 0, m = 1.)  The answer is provided\n    by solving the over-determined matrix equation ``Ax = b``, where::\n\n      A = array([[0, 1], [1, 1], [1, 1], [2, 1]])\n      x = array([[y0], [m]])\n      b = array([[1], [0], [2], [1]])\n\n    If A = qr such that q is orthonormal (which is always possible via\n    Gram-Schmidt), then ``x = inv(r) * (q.T) * b``.  (In numpy practice,\n    however, we simply use `lstsq`.)\n\n    >>> A = np.array([[0, 1], [1, 1], [1, 1], [2, 1]])\n    >>> A\n    array([[0, 1],\n           [1, 1],\n           [1, 1],\n           [2, 1]])\n    >>> b = np.array([1, 0, 2, 1])\n    >>> q, r = np.linalg.qr(A)\n    >>> p = np.dot(q.T, b)\n    >>> np.dot(np.linalg.inv(r), p)\n    array([  1.1e-16,   1.0e+00])\n\n    "
    if (mode not in ('reduced', 'complete', 'r', 'raw')):
        if (mode in ('f', 'full')):
            msg = ''.join(("The 'full' option is deprecated in favor of 'reduced'.\n", 'For backward compatibility let mode default.'))
            warnings.warn(msg, DeprecationWarning, stacklevel=3)
            mode = 'reduced'
        elif (mode in ('e', 'economic')):
            msg = "The 'economic' option is deprecated."
            warnings.warn(msg, DeprecationWarning, stacklevel=3)
            mode = 'economic'
        else:
            raise ValueError(("Unrecognized mode '%s'" % mode))
    (a, wrap) = _makearray(a)
    _assertRank2(a)
    (m, n) = a.shape
    (t, result_t) = _commonType(a)
    a = _fastCopyAndTranspose(t, a)
    a = _to_native_byte_order(a)
    mn = min(m, n)
    tau = zeros((mn,), t)
    if isComplexType(t):
        lapack_routine = lapack_lite.zgeqrf
        routine_name = 'zgeqrf'
    else:
        lapack_routine = lapack_lite.dgeqrf
        routine_name = 'dgeqrf'
    lwork = 1
    work = zeros((lwork,), t)
    results = lapack_routine(m, n, a, max(1, m), tau, work, (- 1), 0)
    if (results['info'] != 0):
        raise LinAlgError(('%s returns %d' % (routine_name, results['info'])))
    lwork = max(1, n, int(abs(work[0])))
    work = zeros((lwork,), t)
    results = lapack_routine(m, n, a, max(1, m), tau, work, lwork, 0)
    if (results['info'] != 0):
        raise LinAlgError(('%s returns %d' % (routine_name, results['info'])))
    if (mode == 'r'):
        r = _fastCopyAndTranspose(result_t, a[:, :mn])
        return wrap(triu(r))
    if (mode == 'raw'):
        return (a, tau)
    if (mode == 'economic'):
        if (t != result_t):
            a = a.astype(result_t, copy=False)
        return wrap(a.T)
    if ((mode == 'complete') and (m > n)):
        mc = m
        q = empty((m, m), t)
    else:
        mc = mn
        q = empty((n, m), t)
    q[:n] = a
    if isComplexType(t):
        lapack_routine = lapack_lite.zungqr
        routine_name = 'zungqr'
    else:
        lapack_routine = lapack_lite.dorgqr
        routine_name = 'dorgqr'
    lwork = 1
    work = zeros((lwork,), t)
    results = lapack_routine(m, mc, mn, q, max(1, m), tau, work, (- 1), 0)
    if (results['info'] != 0):
        raise LinAlgError(('%s returns %d' % (routine_name, results['info'])))
    lwork = max(1, n, int(abs(work[0])))
    work = zeros((lwork,), t)
    results = lapack_routine(m, mc, mn, q, max(1, m), tau, work, lwork, 0)
    if (results['info'] != 0):
        raise LinAlgError(('%s returns %d' % (routine_name, results['info'])))
    q = _fastCopyAndTranspose(result_t, q[:mc])
    r = _fastCopyAndTranspose(result_t, a[:, :mc])
    return (wrap(q), wrap(triu(r)))