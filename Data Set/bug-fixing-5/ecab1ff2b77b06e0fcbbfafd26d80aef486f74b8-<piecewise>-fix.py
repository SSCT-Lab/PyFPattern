def piecewise(x, condlist, funclist, *args, **kw):
    "\n    Evaluate a piecewise-defined function.\n\n    Given a set of conditions and corresponding functions, evaluate each\n    function on the input data wherever its condition is true.\n\n    Parameters\n    ----------\n    x : ndarray or scalar\n        The input domain.\n    condlist : list of bool arrays or bool scalars\n        Each boolean array corresponds to a function in `funclist`.  Wherever\n        `condlist[i]` is True, `funclist[i](x)` is used as the output value.\n\n        Each boolean array in `condlist` selects a piece of `x`,\n        and should therefore be of the same shape as `x`.\n\n        The length of `condlist` must correspond to that of `funclist`.\n        If one extra function is given, i.e. if\n        ``len(funclist) - len(condlist) == 1``, then that extra function\n        is the default value, used wherever all conditions are false.\n    funclist : list of callables, f(x,*args,**kw), or scalars\n        Each function is evaluated over `x` wherever its corresponding\n        condition is True.  It should take an array as input and give an array\n        or a scalar value as output.  If, instead of a callable,\n        a scalar is provided then a constant function (``lambda x: scalar``) is\n        assumed.\n    args : tuple, optional\n        Any further arguments given to `piecewise` are passed to the functions\n        upon execution, i.e., if called ``piecewise(..., ..., 1, 'a')``, then\n        each function is called as ``f(x, 1, 'a')``.\n    kw : dict, optional\n        Keyword arguments used in calling `piecewise` are passed to the\n        functions upon execution, i.e., if called\n        ``piecewise(..., ..., alpha=1)``, then each function is called as\n        ``f(x, alpha=1)``.\n\n    Returns\n    -------\n    out : ndarray\n        The output is the same shape and type as x and is found by\n        calling the functions in `funclist` on the appropriate portions of `x`,\n        as defined by the boolean arrays in `condlist`.  Portions not covered\n        by any condition have a default value of 0.\n\n\n    See Also\n    --------\n    choose, select, where\n\n    Notes\n    -----\n    This is similar to choose or select, except that functions are\n    evaluated on elements of `x` that satisfy the corresponding condition from\n    `condlist`.\n\n    The result is::\n\n            |--\n            |funclist[0](x[condlist[0]])\n      out = |funclist[1](x[condlist[1]])\n            |...\n            |funclist[n2](x[condlist[n2]])\n            |--\n\n    Examples\n    --------\n    Define the sigma function, which is -1 for ``x < 0`` and +1 for ``x >= 0``.\n\n    >>> x = np.linspace(-2.5, 2.5, 6)\n    >>> np.piecewise(x, [x < 0, x >= 0], [-1, 1])\n    array([-1., -1., -1.,  1.,  1.,  1.])\n\n    Define the absolute value, which is ``-x`` for ``x <0`` and ``x`` for\n    ``x >= 0``.\n\n    >>> np.piecewise(x, [x < 0, x >= 0], [lambda x: -x, lambda x: x])\n    array([ 2.5,  1.5,  0.5,  0.5,  1.5,  2.5])\n\n    Apply the same function to a scalar value.\n\n    >>> y = -2\n    >>> np.piecewise(y, [y < 0, y >= 0], [lambda x: -x, lambda x: x])\n    array(2)\n\n    "
    x = asanyarray(x)
    n2 = len(funclist)
    if (isscalar(condlist) or (not (isinstance(condlist[0], list) or isinstance(condlist[0], ndarray)))):
        if ((not isscalar(condlist)) and (x.size == 1) and (x.ndim == 0)):
            condlist = [[c] for c in condlist]
        else:
            condlist = [condlist]
    condlist = array(condlist, dtype=bool)
    n = len(condlist)
    zerod = False
    if (x.ndim == 0):
        x = x[None]
        zerod = True
    if (n == (n2 - 1)):
        condelse = (~ np.any(condlist, axis=0, keepdims=True))
        condlist = np.concatenate([condlist, condelse], axis=0)
        n += 1
    y = zeros(x.shape, x.dtype)
    for k in range(n):
        item = funclist[k]
        if (not isinstance(item, collections.Callable)):
            y[condlist[k]] = item
        else:
            vals = x[condlist[k]]
            if (vals.size > 0):
                y[condlist[k]] = item(vals, *args, **kw)
    if zerod:
        y = y.squeeze()
    return y