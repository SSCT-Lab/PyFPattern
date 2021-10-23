

@array_function_dispatch(_norm_dispatcher)
def norm(x, ord=None, axis=None, keepdims=False):
    "\n    Matrix or vector norm.\n\n    This function is able to return one of eight different matrix norms,\n    or one of an infinite number of vector norms (described below), depending\n    on the value of the ``ord`` parameter.\n\n    Parameters\n    ----------\n    x : array_like\n        Input array.  If `axis` is None, `x` must be 1-D or 2-D.\n    ord : {non-zero int, inf, -inf, 'fro', 'nuc'}, optional\n        Order of the norm (see table under ``Notes``). inf means numpy's\n        `inf` object.\n    axis : {int, 2-tuple of ints, None}, optional\n        If `axis` is an integer, it specifies the axis of `x` along which to\n        compute the vector norms.  If `axis` is a 2-tuple, it specifies the\n        axes that hold 2-D matrices, and the matrix norms of these matrices\n        are computed.  If `axis` is None then either a vector norm (when `x`\n        is 1-D) or a matrix norm (when `x` is 2-D) is returned.\n\n        .. versionadded:: 1.8.0\n\n    keepdims : bool, optional\n        If this is set to True, the axes which are normed over are left in the\n        result as dimensions with size one.  With this option the result will\n        broadcast correctly against the original `x`.\n\n        .. versionadded:: 1.10.0\n\n    Returns\n    -------\n    n : float or ndarray\n        Norm of the matrix or vector(s).\n\n    Notes\n    -----\n    For values of ``ord <= 0``, the result is, strictly speaking, not a\n    mathematical 'norm', but it may still be useful for various numerical\n    purposes.\n\n    The following norms can be calculated:\n\n    =====  ============================  ==========================\n    ord    norm for matrices             norm for vectors\n    =====  ============================  ==========================\n    None   Frobenius norm                2-norm\n    'fro'  Frobenius norm                --\n    'nuc'  nuclear norm                  --\n    inf    max(sum(abs(x), axis=1))      max(abs(x))\n    -inf   min(sum(abs(x), axis=1))      min(abs(x))\n    0      --                            sum(x != 0)\n    1      max(sum(abs(x), axis=0))      as below\n    -1     min(sum(abs(x), axis=0))      as below\n    2      2-norm (largest sing. value)  as below\n    -2     smallest singular value       as below\n    other  --                            sum(abs(x)**ord)**(1./ord)\n    =====  ============================  ==========================\n\n    The Frobenius norm is given by [1]_:\n\n        :math:`||A||_F = [\\sum_{i,j} abs(a_{i,j})^2]^{1/2}`\n\n    The nuclear norm is the sum of the singular values.\n\n    References\n    ----------\n    .. [1] G. H. Golub and C. F. Van Loan, *Matrix Computations*,\n           Baltimore, MD, Johns Hopkins University Press, 1985, pg. 15\n\n    Examples\n    --------\n    >>> from numpy import linalg as LA\n    >>> a = np.arange(9) - 4\n    >>> a\n    array([-4, -3, -2, ...,  2,  3,  4])\n    >>> b = a.reshape((3, 3))\n    >>> b\n    array([[-4, -3, -2],\n           [-1,  0,  1],\n           [ 2,  3,  4]])\n\n    >>> LA.norm(a)\n    7.745966692414834\n    >>> LA.norm(b)\n    7.745966692414834\n    >>> LA.norm(b, 'fro')\n    7.745966692414834\n    >>> LA.norm(a, np.inf)\n    4.0\n    >>> LA.norm(b, np.inf)\n    9.0\n    >>> LA.norm(a, -np.inf)\n    0.0\n    >>> LA.norm(b, -np.inf)\n    2.0\n\n    >>> LA.norm(a, 1)\n    20.0\n    >>> LA.norm(b, 1)\n    7.0\n    >>> LA.norm(a, -1)\n    -4.6566128774142013e-010\n    >>> LA.norm(b, -1)\n    6.0\n    >>> LA.norm(a, 2)\n    7.745966692414834\n    >>> LA.norm(b, 2)\n    7.3484692283495345\n\n    >>> LA.norm(a, -2)\n    0.0\n    >>> LA.norm(b, -2)\n    1.8570331885190563e-016 # may vary\n    >>> LA.norm(a, 3)\n    5.8480354764257312 # may vary\n    >>> LA.norm(a, -3)\n    0.0\n\n    Using the `axis` argument to compute vector norms:\n\n    >>> c = np.array([[ 1, 2, 3],\n    ...               [-1, 1, 4]])\n    >>> LA.norm(c, axis=0)\n    array([ 1.41421356,  2.23606798,  5.        ])\n    >>> LA.norm(c, axis=1)\n    array([ 3.74165739,  4.24264069])\n    >>> LA.norm(c, ord=1, axis=1)\n    array([ 6.,  6.])\n\n    Using the `axis` argument to compute matrix norms:\n\n    >>> m = np.arange(8).reshape(2,2,2)\n    >>> LA.norm(m, axis=(1,2))\n    array([  3.74165739,  11.22497216])\n    >>> LA.norm(m[0, :, :]), LA.norm(m[1, :, :])\n    (3.7416573867739413, 11.224972160321824)\n\n    "
    x = asarray(x)
    if (not issubclass(x.dtype.type, (inexact, object_))):
        x = x.astype(float)
    if (axis is None):
        ndim = x.ndim
        if ((ord is None) or ((ord in ('f', 'fro')) and (ndim == 2)) or ((ord == 2) and (ndim == 1))):
            x = x.ravel(order='K')
            if isComplexType(x.dtype.type):
                sqnorm = (dot(x.real, x.real) + dot(x.imag, x.imag))
            else:
                sqnorm = dot(x, x)
            ret = sqrt(sqnorm)
            if keepdims:
                ret = ret.reshape((ndim * [1]))
            return ret
    nd = x.ndim
    if (axis is None):
        axis = tuple(range(nd))
    elif (not isinstance(axis, tuple)):
        try:
            axis = int(axis)
        except Exception:
            raise TypeError("'axis' must be None, an integer or a tuple of integers")
        axis = (axis,)
    if (len(axis) == 1):
        if (ord == Inf):
            return abs(x).max(axis=axis, keepdims=keepdims)
        elif (ord == (- Inf)):
            return abs(x).min(axis=axis, keepdims=keepdims)
        elif (ord == 0):
            return (x != 0).astype(x.real.dtype).sum(axis=axis, keepdims=keepdims)
        elif (ord == 1):
            return add.reduce(abs(x), axis=axis, keepdims=keepdims)
        elif ((ord is None) or (ord == 2)):
            s = (x.conj() * x).real
            return sqrt(add.reduce(s, axis=axis, keepdims=keepdims))
        else:
            try:
                (ord + 1)
            except TypeError:
                raise ValueError('Invalid norm order for vectors.')
            absx = abs(x)
            absx **= ord
            ret = add.reduce(absx, axis=axis, keepdims=keepdims)
            ret **= (1 / ord)
            return ret
    elif (len(axis) == 2):
        (row_axis, col_axis) = axis
        row_axis = normalize_axis_index(row_axis, nd)
        col_axis = normalize_axis_index(col_axis, nd)
        if (row_axis == col_axis):
            raise ValueError('Duplicate axes given.')
        if (ord == 2):
            ret = _multi_svd_norm(x, row_axis, col_axis, amax)
        elif (ord == (- 2)):
            ret = _multi_svd_norm(x, row_axis, col_axis, amin)
        elif (ord == 1):
            if (col_axis > row_axis):
                col_axis -= 1
            ret = add.reduce(abs(x), axis=row_axis).max(axis=col_axis)
        elif (ord == Inf):
            if (row_axis > col_axis):
                row_axis -= 1
            ret = add.reduce(abs(x), axis=col_axis).max(axis=row_axis)
        elif (ord == (- 1)):
            if (col_axis > row_axis):
                col_axis -= 1
            ret = add.reduce(abs(x), axis=row_axis).min(axis=col_axis)
        elif (ord == (- Inf)):
            if (row_axis > col_axis):
                row_axis -= 1
            ret = add.reduce(abs(x), axis=col_axis).min(axis=row_axis)
        elif (ord in [None, 'fro', 'f']):
            ret = sqrt(add.reduce((x.conj() * x).real, axis=axis))
        elif (ord == 'nuc'):
            ret = _multi_svd_norm(x, row_axis, col_axis, sum)
        else:
            raise ValueError('Invalid norm order for matrices.')
        if keepdims:
            ret_shape = list(x.shape)
            ret_shape[axis[0]] = 1
            ret_shape[axis[1]] = 1
            ret = ret.reshape(ret_shape)
        return ret
    else:
        raise ValueError('Improper number of dimensions to norm.')
