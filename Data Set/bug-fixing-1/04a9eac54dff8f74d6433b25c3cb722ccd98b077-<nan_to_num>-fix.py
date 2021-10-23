

def nan_to_num(x):
    '\n    Replace nan with zero and inf with finite numbers.\n\n    Returns an array or scalar replacing Not a Number (NaN) with zero,\n    (positive) infinity with a very large number and negative infinity\n    with a very small (or negative) number.\n\n    Parameters\n    ----------\n    x : array_like\n        Input data.\n\n    Returns\n    -------\n    out : ndarray\n        New Array with the same shape as `x` and dtype of the element in\n        `x`  with the greatest precision. If `x` is inexact, then NaN is\n        replaced by zero, and infinity (-infinity) is replaced by the\n        largest (smallest or most negative) floating point value that fits\n        in the output dtype. If `x` is not inexact, then a copy of `x` is\n        returned.\n\n    See Also\n    --------\n    isinf : Shows which elements are positive or negative infinity.\n    isneginf : Shows which elements are negative infinity.\n    isposinf : Shows which elements are positive infinity.\n    isnan : Shows which elements are Not a Number (NaN).\n    isfinite : Shows which elements are finite (not NaN, not infinity)\n\n    Notes\n    -----\n    NumPy uses the IEEE Standard for Binary Floating-Point for Arithmetic\n    (IEEE 754). This means that Not a Number is not equivalent to infinity.\n\n\n    Examples\n    --------\n    >>> np.set_printoptions(precision=8)\n    >>> x = np.array([np.inf, -np.inf, np.nan, -128, 128])\n    >>> np.nan_to_num(x)\n    array([  1.79769313e+308,  -1.79769313e+308,   0.00000000e+000,\n            -1.28000000e+002,   1.28000000e+002])\n\n    '
    x = _nx.array(x, subok=True)
    xtype = x.dtype.type
    if (not issubclass(xtype, _nx.inexact)):
        return x
    iscomplex = issubclass(xtype, _nx.complexfloating)
    isscalar = (x.ndim == 0)
    x = (x[None] if isscalar else x)
    dest = ((x.real, x.imag) if iscomplex else (x,))
    (maxf, minf) = _getmaxmin(x.real.dtype)
    for d in dest:
        _nx.copyto(d, 0.0, where=isnan(d))
        _nx.copyto(d, maxf, where=isposinf(d))
        _nx.copyto(d, minf, where=isneginf(d))
    return (x[0] if isscalar else x)
