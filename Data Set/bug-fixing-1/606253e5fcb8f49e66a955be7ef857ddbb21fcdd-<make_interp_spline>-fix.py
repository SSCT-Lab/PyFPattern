

def make_interp_spline(x, y, k=3, t=None, bc_type=None, axis=0, check_finite=True):
    'Compute the (coefficients of) interpolating B-spline.\n\n    Parameters\n    ----------\n    x : array_like, shape (n,)\n        Abscissas.\n    y : array_like, shape (n, ...)\n        Ordinates.\n    k : int, optional\n        B-spline degree. Default is cubic, k=3.\n    t : array_like, shape (nt + k + 1,), optional.\n        Knots.\n        The number of knots needs to agree with the number of datapoints and\n        the number of derivatives at the edges. Specifically, ``nt - n`` must\n        equal ``len(deriv_l) + len(deriv_r)``.\n    bc_type : 2-tuple or None\n        Boundary conditions.\n        Default is None, which means choosing the boundary conditions\n        automatically. Otherwise, it must be a length-two tuple where the first\n        element sets the boundary conditions at ``x[0]`` and the second\n        element sets the boundary conditions at ``x[-1]``. Each of these must\n        be an iterable of pairs ``(order, value)`` which gives the values of\n        derivatives of specified orders at the given edge of the interpolation\n        interval.\n        Alternatively, the following string aliases are recognized:\n\n        * ``"clamped"``: The first derivatives at the ends are zero. This is\n           equivalent to ``bc_type=([(1, 0.0)], [(1, 0.0)])``.\n        * ``"natural"``: The second derivatives at ends are zero. This is\n          equivalent to ``bc_type=([(2, 0.0)], [(2, 0.0)])``.\n        * ``"not-a-knot"`` (default): The first and second segments are the same\n          polynomial. This is equivalent to having ``bc_type=None``.\n\n    axis : int, optional\n        Interpolation axis. Default is 0.\n    check_finite : bool, optional\n        Whether to check that the input arrays contain only finite numbers.\n        Disabling may give a performance gain, but may result in problems\n        (crashes, non-termination) if the inputs do contain infinities or NaNs.\n        Default is True.\n\n    Returns\n    -------\n    b : a BSpline object of the degree ``k`` and with knots ``t``.\n\n    Examples\n    --------\n\n    Use cubic interpolation on Chebyshev nodes:\n\n    >>> def cheb_nodes(N):\n    ...     jj = 2.*np.arange(N) + 1\n    ...     x = np.cos(np.pi * jj / 2 / N)[::-1]\n    ...     return x\n\n    >>> x = cheb_nodes(20)\n    >>> y = np.sqrt(1 - x**2)\n\n    >>> from scipy.interpolate import BSpline, make_interp_spline\n    >>> b = make_interp_spline(x, y)\n    >>> np.allclose(b(x), y)\n    True\n\n    Note that the default is a cubic spline with a not-a-knot boundary condition\n\n    >>> b.k\n    3\n\n    Here we use a \'natural\' spline, with zero 2nd derivatives at edges:\n\n    >>> l, r = [(2, 0.0)], [(2, 0.0)]\n    >>> b_n = make_interp_spline(x, y, bc_type=(l, r))  # or, bc_type="natural"\n    >>> np.allclose(b_n(x), y)\n    True\n    >>> x0, x1 = x[0], x[-1]\n    >>> np.allclose([b_n(x0, 2), b_n(x1, 2)], [0, 0])\n    True\n\n    Interpolation of parametric curves is also supported. As an example, we\n    compute a discretization of a snail curve in polar coordinates\n\n    >>> phi = np.linspace(0, 2.*np.pi, 40)\n    >>> r = 0.3 + np.cos(phi)\n    >>> x, y = r*np.cos(phi), r*np.sin(phi)  # convert to Cartesian coordinates\n\n    Build an interpolating curve, parameterizing it by the angle\n\n    >>> from scipy.interpolate import make_interp_spline\n    >>> spl = make_interp_spline(phi, np.c_[x, y])\n\n    Evaluate the interpolant on a finer grid (note that we transpose the result\n    to unpack it into a pair of x- and y-arrays)\n\n    >>> phi_new = np.linspace(0, 2.*np.pi, 100)\n    >>> x_new, y_new = spl(phi_new).T\n\n    Plot the result\n\n    >>> import matplotlib.pyplot as plt\n    >>> plt.plot(x, y, \'o\')\n    >>> plt.plot(x_new, y_new, \'-\')\n    >>> plt.show()\n\n    See Also\n    --------\n    BSpline : base class representing the B-spline objects\n    CubicSpline : a cubic spline in the polynomial basis\n    make_lsq_spline : a similar factory function for spline fitting\n    UnivariateSpline : a wrapper over FITPACK spline fitting routines\n    splrep : a wrapper over FITPACK spline fitting routines\n\n    '
    if ((bc_type is None) or (bc_type == 'not-a-knot')):
        (deriv_l, deriv_r) = (None, None)
    elif isinstance(bc_type, string_types):
        (deriv_l, deriv_r) = (bc_type, bc_type)
    else:
        (deriv_l, deriv_r) = bc_type
    if (k == 0):
        if any(((_ is not None) for _ in (t, deriv_l, deriv_r))):
            raise ValueError('Too much info for k=0: t and bc_type can only be None.')
        x = _as_float_array(x, check_finite)
        t = np.r_[(x, x[(- 1)])]
        c = np.asarray(y)
        c = np.ascontiguousarray(c, dtype=_get_dtype(c.dtype))
        return BSpline.construct_fast(t, c, k, axis=axis)
    if ((k == 1) and (t is None)):
        if (not ((deriv_l is None) and (deriv_r is None))):
            raise ValueError('Too much info for k=1: bc_type can only be None.')
        x = _as_float_array(x, check_finite)
        t = np.r_[(x[0], x, x[(- 1)])]
        c = np.asarray(y)
        c = np.ascontiguousarray(c, dtype=_get_dtype(c.dtype))
        return BSpline.construct_fast(t, c, k, axis=axis)
    x = _as_float_array(x, check_finite)
    y = _as_float_array(y, check_finite)
    k = int(k)
    if (t is None):
        if ((deriv_l is None) and (deriv_r is None)):
            if (k == 2):
                t = ((x[1:] + x[:(- 1)]) / 2.0)
                t = np.r_[(((x[0],) * (k + 1)), t[1:(- 1)], ((x[(- 1)],) * (k + 1)))]
            else:
                t = _not_a_knot(x, k)
        else:
            t = _augknt(x, k)
    t = _as_float_array(t, check_finite)
    axis = (axis % y.ndim)
    y = np.rollaxis(y, axis)
    if ((x.ndim != 1) or np.any((x[1:] <= x[:(- 1)]))):
        raise ValueError('Expect x to be a 1-D sorted array_like.')
    if (k < 0):
        raise ValueError('Expect non-negative k.')
    if ((t.ndim != 1) or np.any((t[1:] < t[:(- 1)]))):
        raise ValueError('Expect t to be a 1-D sorted array_like.')
    if (x.size != y.shape[0]):
        raise ValueError('x and y are incompatible.')
    if (t.size < ((x.size + k) + 1)):
        raise ValueError(('Got %d knots, need at least %d.' % (t.size, ((x.size + k) + 1))))
    if ((x[0] < t[k]) or (x[(- 1)] > t[(- k)])):
        raise ValueError(('Out of bounds w/ x = %s.' % x))
    deriv_l = _convert_string_aliases(deriv_l, y.shape[1:])
    if (deriv_l is not None):
        (deriv_l_ords, deriv_l_vals) = zip(*deriv_l)
    else:
        (deriv_l_ords, deriv_l_vals) = ([], [])
    (deriv_l_ords, deriv_l_vals) = np.atleast_1d(deriv_l_ords, deriv_l_vals)
    nleft = deriv_l_ords.shape[0]
    deriv_r = _convert_string_aliases(deriv_r, y.shape[1:])
    if (deriv_r is not None):
        (deriv_r_ords, deriv_r_vals) = zip(*deriv_r)
    else:
        (deriv_r_ords, deriv_r_vals) = ([], [])
    (deriv_r_ords, deriv_r_vals) = np.atleast_1d(deriv_r_ords, deriv_r_vals)
    nright = deriv_r_ords.shape[0]
    n = x.size
    nt = ((t.size - k) - 1)
    if ((nt - n) != (nleft + nright)):
        raise ValueError('number of derivatives at boundaries.')
    kl = ku = k
    ab = np.zeros(((((2 * kl) + ku) + 1), nt), dtype=np.float_, order='F')
    _bspl._colloc(x, t, k, ab, offset=nleft)
    if (nleft > 0):
        _bspl._handle_lhs_derivatives(t, k, x[0], ab, kl, ku, deriv_l_ords)
    if (nright > 0):
        _bspl._handle_lhs_derivatives(t, k, x[(- 1)], ab, kl, ku, deriv_r_ords, offset=(nt - nright))
    extradim = prod(y.shape[1:])
    rhs = np.empty((nt, extradim), dtype=y.dtype)
    if (nleft > 0):
        rhs[:nleft] = deriv_l_vals.reshape((- 1), extradim)
    rhs[nleft:(nt - nright)] = y.reshape((- 1), extradim)
    if (nright > 0):
        rhs[(nt - nright):] = deriv_r_vals.reshape((- 1), extradim)
    if check_finite:
        (ab, rhs) = map(np.asarray_chkfinite, (ab, rhs))
    (gbsv,) = get_lapack_funcs(('gbsv',), (ab, rhs))
    (lu, piv, c, info) = gbsv(kl, ku, ab, rhs, overwrite_ab=True, overwrite_b=True)
    if (info > 0):
        raise LinAlgError('Collocation matix is singular.')
    elif (info < 0):
        raise ValueError(('illegal value in %d-th argument of internal gbsv' % (- info)))
    c = np.ascontiguousarray(c.reshape(((nt,) + y.shape[1:])))
    return BSpline.construct_fast(t, c, k, axis=axis)
