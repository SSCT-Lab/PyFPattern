

def chebfit(x, y, deg, rcond=None, full=False, w=None):
    '\n    Least squares fit of Chebyshev series to data.\n\n    Return the coefficients of a Legendre series of degree `deg` that is the\n    least squares fit to the data values `y` given at points `x`. If `y` is\n    1-D the returned coefficients will also be 1-D. If `y` is 2-D multiple\n    fits are done, one for each column of `y`, and the resulting\n    coefficients are stored in the corresponding columns of a 2-D return.\n    The fitted polynomial(s) are in the form\n\n    .. math::  p(x) = c_0 + c_1 * T_1(x) + ... + c_n * T_n(x),\n\n    where `n` is `deg`.\n\n    Parameters\n    ----------\n    x : array_like, shape (M,)\n        x-coordinates of the M sample points ``(x[i], y[i])``.\n    y : array_like, shape (M,) or (M, K)\n        y-coordinates of the sample points. Several data sets of sample\n        points sharing the same x-coordinates can be fitted at once by\n        passing in a 2D-array that contains one dataset per column.\n    deg : int or 1-D array_like\n        Degree(s) of the fitting polynomials. If `deg` is a single integer\n        all terms up to and including the `deg`\'th term are included in the\n        fit. For NumPy versions >= 1.11.0 a list of integers specifying the\n        degrees of the terms to include may be used instead.\n    rcond : float, optional\n        Relative condition number of the fit. Singular values smaller than\n        this relative to the largest singular value will be ignored. The\n        default value is len(x)*eps, where eps is the relative precision of\n        the float type, about 2e-16 in most cases.\n    full : bool, optional\n        Switch determining nature of return value. When it is False (the\n        default) just the coefficients are returned, when True diagnostic\n        information from the singular value decomposition is also returned.\n    w : array_like, shape (`M`,), optional\n        Weights. If not None, the contribution of each point\n        ``(x[i],y[i])`` to the fit is weighted by `w[i]`. Ideally the\n        weights are chosen so that the errors of the products ``w[i]*y[i]``\n        all have the same variance.  The default value is None.\n\n        .. versionadded:: 1.5.0\n\n    Returns\n    -------\n    coef : ndarray, shape (M,) or (M, K)\n        Chebyshev coefficients ordered from low to high. If `y` was 2-D,\n        the coefficients for the data in column k  of `y` are in column\n        `k`.\n\n    [residuals, rank, singular_values, rcond] : list\n        These values are only returned if `full` = True\n\n        resid -- sum of squared residuals of the least squares fit\n        rank -- the numerical rank of the scaled Vandermonde matrix\n        sv -- singular values of the scaled Vandermonde matrix\n        rcond -- value of `rcond`.\n\n        For more details, see `linalg.lstsq`.\n\n    Warns\n    -----\n    RankWarning\n        The rank of the coefficient matrix in the least-squares fit is\n        deficient. The warning is only raised if `full` = False.  The\n        warnings can be turned off by\n\n        >>> import warnings\n        >>> warnings.simplefilter(\'ignore\', RankWarning)\n\n    See Also\n    --------\n    polyfit, legfit, lagfit, hermfit, hermefit\n    chebval : Evaluates a Chebyshev series.\n    chebvander : Vandermonde matrix of Chebyshev series.\n    chebweight : Chebyshev weight function.\n    linalg.lstsq : Computes a least-squares fit from the matrix.\n    scipy.interpolate.UnivariateSpline : Computes spline fits.\n\n    Notes\n    -----\n    The solution is the coefficients of the Chebyshev series `p` that\n    minimizes the sum of the weighted squared errors\n\n    .. math:: E = \\sum_j w_j^2 * |y_j - p(x_j)|^2,\n\n    where :math:`w_j` are the weights. This problem is solved by setting up\n    as the (typically) overdetermined matrix equation\n\n    .. math:: V(x) * c = w * y,\n\n    where `V` is the weighted pseudo Vandermonde matrix of `x`, `c` are the\n    coefficients to be solved for, `w` are the weights, and `y` are the\n    observed values.  This equation is then solved using the singular value\n    decomposition of `V`.\n\n    If some of the singular values of `V` are so small that they are\n    neglected, then a `RankWarning` will be issued. This means that the\n    coefficient values may be poorly determined. Using a lower order fit\n    will usually get rid of the warning.  The `rcond` parameter can also be\n    set to a value smaller than its default, but the resulting fit may be\n    spurious and have large contributions from roundoff error.\n\n    Fits using Chebyshev series are usually better conditioned than fits\n    using power series, but much can depend on the distribution of the\n    sample points and the smoothness of the data. If the quality of the fit\n    is inadequate splines may be a good alternative.\n\n    References\n    ----------\n    .. [1] Wikipedia, "Curve fitting",\n           http://en.wikipedia.org/wiki/Curve_fitting\n\n    Examples\n    --------\n\n    '
    x = (np.asarray(x) + 0.0)
    y = (np.asarray(y) + 0.0)
    deg = np.asarray(deg)
    if ((deg.ndim > 1) or (deg.dtype.kind not in 'iu') or (deg.size == 0)):
        raise TypeError('deg must be an int or non-empty 1-D array of int')
    if (deg.min() < 0):
        raise ValueError('expected deg >= 0')
    if (x.ndim != 1):
        raise TypeError('expected 1D vector for x')
    if (x.size == 0):
        raise TypeError('expected non-empty vector for x')
    if ((y.ndim < 1) or (y.ndim > 2)):
        raise TypeError('expected 1D or 2D array for y')
    if (len(x) != len(y)):
        raise TypeError('expected x and y to have same length')
    if (deg.ndim == 0):
        lmax = deg
        order = (lmax + 1)
        van = chebvander(x, lmax)
    else:
        deg = np.sort(deg)
        lmax = deg[(- 1)]
        order = len(deg)
        van = chebvander(x, lmax)[:, deg]
    lhs = van.T
    rhs = y.T
    if (w is not None):
        w = (np.asarray(w) + 0.0)
        if (w.ndim != 1):
            raise TypeError('expected 1D vector for w')
        if (len(x) != len(w)):
            raise TypeError('expected x and w to have same length')
        lhs = (lhs * w)
        rhs = (rhs * w)
    if (rcond is None):
        rcond = (len(x) * np.finfo(x.dtype).eps)
    if issubclass(lhs.dtype.type, np.complexfloating):
        scl = np.sqrt((np.square(lhs.real) + np.square(lhs.imag)).sum(1))
    else:
        scl = np.sqrt(np.square(lhs).sum(1))
    scl[(scl == 0)] = 1
    (c, resids, rank, s) = la.lstsq((lhs.T / scl), rhs.T, rcond)
    c = (c.T / scl).T
    if (deg.ndim > 0):
        if (c.ndim == 2):
            cc = np.zeros(((lmax + 1), c.shape[1]), dtype=c.dtype)
        else:
            cc = np.zeros((lmax + 1), dtype=c.dtype)
        cc[deg] = c
        c = cc
    if ((rank != order) and (not full)):
        msg = 'The fit may be poorly conditioned'
        warnings.warn(msg, pu.RankWarning, stacklevel=2)
    if full:
        return (c, [resids, rank, s, rcond])
    else:
        return c
