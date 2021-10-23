

def idstn(x, type=2, shape=None, axes=None, norm=None, overwrite_x=False):
    "\n    Return multidimensional Discrete Sine Transform along the specified axes.\n\n    Parameters\n    ----------\n    x : array_like\n        The input array.\n    type : {1, 2, 3, 4}, optional\n        Type of the DST (see Notes). Default type is 2.\n    shape : int or array_like of ints or None, optional\n        The shape of the result.  If both `shape` and `axes` (see below) are\n        None, `shape` is ``x.shape``; if `shape` is None but `axes` is\n        not None, then `shape` is ``scipy.take(x.shape, axes, axis=0)``.\n        If ``shape[i] > x.shape[i]``, the i-th dimension is padded with zeros.\n        If ``shape[i] < x.shape[i]``, the i-th dimension is truncated to\n        length ``shape[i]``.\n        If any element of `shape` is -1, the size of the corresponding\n        dimension of `x` is used.\n    axes : int or array_like of ints or None, optional\n        Axes along which the IDST is computed.\n        The default is over all axes.\n    norm : {None, 'ortho'}, optional\n        Normalization mode (see Notes). Default is None.\n    overwrite_x : bool, optional\n        If True, the contents of `x` can be destroyed; the default is False.\n\n    Returns\n    -------\n    y : ndarray of real\n        The transformed input array.\n\n    See Also\n    --------\n    dstn : multidimensional DST\n\n    Notes\n    -----\n    For full details of the IDST types and normalization modes, as well as\n    references, see `idst`.\n\n    Examples\n    --------\n    >>> from scipy.fftpack import dstn, idstn\n    >>> y = np.random.randn(16, 16)\n    >>> np.allclose(y, idstn(dstn(y, norm='ortho'), norm='ortho'))\n    True\n\n    "
    x = np.asanyarray(x)
    (shape, axes) = _init_nd_shape_and_axes(x, shape, axes)
    for (n, ax) in zip(shape, axes):
        x = idst(x, type=type, n=n, axis=ax, norm=norm, overwrite_x=overwrite_x)
    return x
