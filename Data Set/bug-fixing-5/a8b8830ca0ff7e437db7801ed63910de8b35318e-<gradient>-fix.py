def gradient(f, *varargs, **kwargs):
    '\n    Return the gradient of an N-dimensional array.\n\n    The gradient is computed using second order accurate central differences\n    in the interior points and either first or second order accurate one-sides\n    (forward or backwards) differences at the boundaries.\n    The returned gradient hence has the same shape as the input array.\n\n    Parameters\n    ----------\n    f : array_like\n        An N-dimensional array containing samples of a scalar function.\n    varargs : list of scalar or array, optional\n        Spacing between f values. Default unitary spacing for all dimensions.\n        Spacing can be specified using:\n\n        1. single scalar to specify a sample distance for all dimensions.\n        2. N scalars to specify a constant sample distance for each dimension.\n           i.e. `dx`, `dy`, `dz`, ...\n        3. N arrays to specify the coordinates of the values along each\n           dimension of F. The length of the array must match the size of\n           the corresponding dimension\n        4. Any combination of N scalars/arrays with the meaning of 2. and 3.\n\n        If `axis` is given, the number of varargs must equal the number of axes.\n        Default: 1.\n\n    edge_order : {1, 2}, optional\n        Gradient is calculated using N-th order accurate differences\n        at the boundaries. Default: 1.\n\n        .. versionadded:: 1.9.1\n\n    axis : None or int or tuple of ints, optional\n        Gradient is calculated only along the given axis or axes\n        The default (axis = None) is to calculate the gradient for all the axes\n        of the input array. axis may be negative, in which case it counts from\n        the last to the first axis.\n\n        .. versionadded:: 1.11.0\n\n    Returns\n    -------\n    gradient : ndarray or list of ndarray\n        A set of ndarrays (or a single ndarray if there is only one dimension)\n        corresponding to the derivatives of f with respect to each dimension.\n        Each derivative has the same shape as f.\n\n    Examples\n    --------\n    >>> f = np.array([1, 2, 4, 7, 11, 16], dtype=float)\n    >>> np.gradient(f)\n    array([ 1. ,  1.5,  2.5,  3.5,  4.5,  5. ])\n    >>> np.gradient(f, 2)\n    array([ 0.5 ,  0.75,  1.25,  1.75,  2.25,  2.5 ])\n\n    Spacing can be also specified with an array that represents the coordinates\n    of the values F along the dimensions.\n    For instance a uniform spacing:\n\n    >>> x = np.arange(f.size)\n    >>> np.gradient(f, x)\n    array([ 1. ,  1.5,  2.5,  3.5,  4.5,  5. ])\n\n    Or a non uniform one:\n\n    >>> x = np.array([0., 1., 1.5, 3.5, 4., 6.], dtype=float)\n    >>> np.gradient(f, x)\n    array([ 1. ,  3. ,  3.5,  6.7,  6.9,  2.5])\n\n    For two dimensional arrays, the return will be two arrays ordered by\n    axis. In this example the first array stands for the gradient in\n    rows and the second one in columns direction:\n\n    >>> np.gradient(np.array([[1, 2, 6], [3, 4, 5]], dtype=float))\n    [array([[ 2.,  2., -1.],\n            [ 2.,  2., -1.]]), array([[ 1. ,  2.5,  4. ],\n            [ 1. ,  1. ,  1. ]])]\n\n    In this example the spacing is also specified:\n    uniform for axis=0 and non uniform for axis=1\n\n    >>> dx = 2.\n    >>> y = [1., 1.5, 3.5]\n    >>> np.gradient(np.array([[1, 2, 6], [3, 4, 5]], dtype=float), dx, y)\n    [array([[ 1. ,  1. , -0.5],\n            [ 1. ,  1. , -0.5]]), array([[ 2. ,  2. ,  2. ],\n            [ 2. ,  1.7,  0.5]])]\n\n    It is possible to specify how boundaries are treated using `edge_order`\n\n    >>> x = np.array([0, 1, 2, 3, 4])\n    >>> f = x**2\n    >>> np.gradient(f, edge_order=1)\n    array([ 1.,  2.,  4.,  6.,  7.])\n    >>> np.gradient(f, edge_order=2)\n    array([-0.,  2.,  4.,  6.,  8.])\n\n    The `axis` keyword can be used to specify a subset of axes of which the\n    gradient is calculated\n\n    >>> np.gradient(np.array([[1, 2, 6], [3, 4, 5]], dtype=float), axis=0)\n    array([[ 2.,  2., -1.],\n           [ 2.,  2., -1.]])\n\n    Notes\n    -----\n    Assuming that :math:`f\\in C^{3}` (i.e., :math:`f` has at least 3 continuous\n    derivatives) and let be :math:`h_{*}` a non homogeneous stepsize, the\n    spacing the finite difference coefficients are computed by minimising\n    the consistency error :math:`\\eta_{i}`:\n\n    .. math::\n\n        \\eta_{i} = f_{i}^{\\left(1\\right)} -\n                    \\left[ \\alpha f\\left(x_{i}\\right) +\n                            \\beta f\\left(x_{i} + h_{d}\\right) +\n                            \\gamma f\\left(x_{i}-h_{s}\\right)\n                    \\right]\n\n    By substituting :math:`f(x_{i} + h_{d})` and :math:`f(x_{i} - h_{s})`\n    with their Taylor series expansion, this translates into solving\n    the following the linear system:\n\n    .. math::\n\n        \\left\\{\n            \\begin{array}{r}\n                \\alpha+\\beta+\\gamma=0 \\\\\n                \\beta h_{d}-\\gamma h_{s}=1 \\\\\n                \\beta h_{d}^{2}+\\gamma h_{s}^{2}=0\n            \\end{array}\n        \\right.\n\n    The resulting approximation of :math:`f_{i}^{(1)}` is the following:\n\n    .. math::\n\n        \\hat f_{i}^{(1)} =\n            \\frac{\n                h_{s}^{2}f\\left(x_{i} + h_{d}\\right)\n                + \\left(h_{d}^{2} - h_{s}^{2}\\right)f\\left(x_{i}\\right)\n                - h_{d}^{2}f\\left(x_{i}-h_{s}\\right)}\n                { h_{s}h_{d}\\left(h_{d} + h_{s}\\right)}\n            + \\mathcal{O}\\left(\\frac{h_{d}h_{s}^{2}\n                                + h_{s}h_{d}^{2}}{h_{d}\n                                + h_{s}}\\right)\n\n    It is worth noting that if :math:`h_{s}=h_{d}`\n    (i.e., data are evenly spaced)\n    we find the standard second order approximation:\n\n    .. math::\n\n        \\hat f_{i}^{(1)}=\n            \\frac{f\\left(x_{i+1}\\right) - f\\left(x_{i-1}\\right)}{2h}\n            + \\mathcal{O}\\left(h^{2}\\right)\n\n    With a similar procedure the forward/backward approximations used for\n    boundaries can be derived.\n\n    References\n    ----------\n    .. [1]  Quarteroni A., Sacco R., Saleri F. (2007) Numerical Mathematics\n            (Texts in Applied Mathematics). New York: Springer.\n    .. [2]  Durran D. R. (1999) Numerical Methods for Wave Equations\n            in Geophysical Fluid Dynamics. New York: Springer.\n    .. [3]  Fornberg B. (1988) Generation of Finite Difference Formulas on\n            Arbitrarily Spaced Grids,\n            Mathematics of Computation 51, no. 184 : 699-706.\n            `PDF <http://www.ams.org/journals/mcom/1988-51-184/\n            S0025-5718-1988-0935077-0/S0025-5718-1988-0935077-0.pdf>`_.\n    '
    f = np.asanyarray(f)
    N = f.ndim
    axes = kwargs.pop('axis', None)
    if (axes is None):
        axes = tuple(range(N))
    else:
        axes = _nx.normalize_axis_tuple(axes, N)
    len_axes = len(axes)
    n = len(varargs)
    if (n == 0):
        dx = ([1.0] * len_axes)
    elif ((n == 1) and (np.ndim(varargs[0]) == 0)):
        dx = (varargs * len_axes)
    elif (n == len_axes):
        dx = list(varargs)
        for (i, distances) in enumerate(dx):
            if (np.ndim(distances) == 0):
                continue
            elif (np.ndim(distances) != 1):
                raise ValueError('distances must be either scalars or 1d')
            if (len(distances) != f.shape[axes[i]]):
                raise ValueError('when 1d, distances must match the length of the corresponding dimension')
            diffx = np.diff(distances)
            if (diffx == diffx[0]).all():
                diffx = diffx[0]
            dx[i] = diffx
    else:
        raise TypeError('invalid number of arguments')
    edge_order = kwargs.pop('edge_order', 1)
    if kwargs:
        raise TypeError('"{}" are not valid keyword arguments.'.format('", "'.join(kwargs.keys())))
    if (edge_order > 2):
        raise ValueError("'edge_order' greater than 2 not supported")
    outvals = []
    slice1 = ([slice(None)] * N)
    slice2 = ([slice(None)] * N)
    slice3 = ([slice(None)] * N)
    slice4 = ([slice(None)] * N)
    otype = f.dtype
    if (otype.type is np.datetime64):
        otype = np.dtype(otype.name.replace('datetime', 'timedelta'))
        f = f.view(otype)
    elif (otype.type is np.timedelta64):
        pass
    elif np.issubdtype(otype, np.inexact):
        pass
    else:
        otype = np.double
    for (axis, ax_dx) in zip(axes, dx):
        if (f.shape[axis] < (edge_order + 1)):
            raise ValueError('Shape of array too small to calculate a numerical gradient, at least (edge_order + 1) elements are required.')
        out = np.empty_like(f, dtype=otype)
        uniform_spacing = (np.ndim(ax_dx) == 0)
        slice1[axis] = slice(1, (- 1))
        slice2[axis] = slice(None, (- 2))
        slice3[axis] = slice(1, (- 1))
        slice4[axis] = slice(2, None)
        if uniform_spacing:
            out[slice1] = ((f[slice4] - f[slice2]) / (2.0 * ax_dx))
        else:
            dx1 = ax_dx[0:(- 1)]
            dx2 = ax_dx[1:]
            a = ((- dx2) / (dx1 * (dx1 + dx2)))
            b = ((dx2 - dx1) / (dx1 * dx2))
            c = (dx1 / (dx2 * (dx1 + dx2)))
            shape = np.ones(N, dtype=int)
            shape[axis] = (- 1)
            a.shape = b.shape = c.shape = shape
            out[slice1] = (((a * f[slice2]) + (b * f[slice3])) + (c * f[slice4]))
        if (edge_order == 1):
            slice1[axis] = 0
            slice2[axis] = 1
            slice3[axis] = 0
            dx_0 = (ax_dx if uniform_spacing else ax_dx[0])
            out[slice1] = ((f[slice2] - f[slice3]) / dx_0)
            slice1[axis] = (- 1)
            slice2[axis] = (- 1)
            slice3[axis] = (- 2)
            dx_n = (ax_dx if uniform_spacing else ax_dx[(- 1)])
            out[slice1] = ((f[slice2] - f[slice3]) / dx_n)
        else:
            slice1[axis] = 0
            slice2[axis] = 0
            slice3[axis] = 1
            slice4[axis] = 2
            if uniform_spacing:
                a = ((- 1.5) / ax_dx)
                b = (2.0 / ax_dx)
                c = ((- 0.5) / ax_dx)
            else:
                dx1 = ax_dx[0]
                dx2 = ax_dx[1]
                a = ((- ((2.0 * dx1) + dx2)) / (dx1 * (dx1 + dx2)))
                b = ((dx1 + dx2) / (dx1 * dx2))
                c = ((- dx1) / (dx2 * (dx1 + dx2)))
            out[slice1] = (((a * f[slice2]) + (b * f[slice3])) + (c * f[slice4]))
            slice1[axis] = (- 1)
            slice2[axis] = (- 3)
            slice3[axis] = (- 2)
            slice4[axis] = (- 1)
            if uniform_spacing:
                a = (0.5 / ax_dx)
                b = ((- 2.0) / ax_dx)
                c = (1.5 / ax_dx)
            else:
                dx1 = ax_dx[(- 2)]
                dx2 = ax_dx[(- 1)]
                a = (dx2 / (dx1 * (dx1 + dx2)))
                b = ((- (dx2 + dx1)) / (dx1 * dx2))
                c = (((2.0 * dx2) + dx1) / (dx2 * (dx1 + dx2)))
            out[slice1] = (((a * f[slice2]) + (b * f[slice3])) + (c * f[slice4]))
        outvals.append(out)
        slice1[axis] = slice(None)
        slice2[axis] = slice(None)
        slice3[axis] = slice(None)
        slice4[axis] = slice(None)
    if (len_axes == 1):
        return outvals[0]
    else:
        return outvals