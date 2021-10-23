def corrcoef(x, y=None, rowvar=1, bias=np._NoValue, ddof=np._NoValue):
    '\n    Return Pearson product-moment correlation coefficients.\n\n    Please refer to the documentation for `cov` for more detail.  The\n    relationship between the correlation coefficient matrix, `R`, and the\n    covariance matrix, `C`, is\n\n    .. math:: R_{ij} = \\frac{ C_{ij} } { \\sqrt{ C_{ii} * C_{jj} } }\n\n    The values of `R` are between -1 and 1, inclusive.\n\n    Parameters\n    ----------\n    x : array_like\n        A 1-D or 2-D array containing multiple variables and observations.\n        Each row of `x` represents a variable, and each column a single\n        observation of all those variables. Also see `rowvar` below.\n    y : array_like, optional\n        An additional set of variables and observations. `y` has the same\n        shape as `x`.\n    rowvar : int, optional\n        If `rowvar` is non-zero (default), then each row represents a\n        variable, with observations in the columns. Otherwise, the relationship\n        is transposed: each column represents a variable, while the rows\n        contain observations.\n    bias : _NoValue, optional\n        Has no effect, do not use.\n\n        .. deprecated:: 1.10.0\n    ddof : _NoValue, optional\n        Has no effect, do not use.\n\n        .. deprecated:: 1.10.0\n\n    Returns\n    -------\n    R : ndarray\n        The correlation coefficient matrix of the variables.\n\n    See Also\n    --------\n    cov : Covariance matrix\n\n    Notes\n    -----\n    Due to floating point rounding the resulting array may not be Hermitian,\n    the diagonal elements may not be 1, and the elements may not satisfy the\n    inequality abs(a) <= 1. The real and imaginary parts are clipped to the\n    interval [-1,  1] in an attempt to improve on that situation but is not\n    much help in the complex case.\n\n    This function accepts but discards arguments `bias` and `ddof`.  This is\n    for backwards compatibility with previous versions of this function.  These\n    arguments had no effect on the return values of the function and can be\n    safely ignored in this and previous versions of numpy.\n\n    '
    if ((bias is not np._NoValue) or (ddof is not np._NoValue)):
        warnings.warn('bias and ddof have no effect and are deprecated', DeprecationWarning, stacklevel=2)
    c = cov(x, y, rowvar)
    try:
        d = diag(c)
    except ValueError:
        return (c / c)
    stddev = sqrt(d.real)
    c /= stddev[:, None]
    c /= stddev[None, :]
    np.clip(c.real, (- 1), 1, out=c.real)
    if np.iscomplexobj(c):
        np.clip(c.imag, (- 1), 1, out=c.imag)
    return c