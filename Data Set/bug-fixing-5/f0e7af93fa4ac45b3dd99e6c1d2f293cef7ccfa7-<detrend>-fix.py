def detrend(data, axis=(- 1), type='linear', bp=0, overwrite_data=False):
    "\n    Remove linear trend along axis from data.\n\n    Parameters\n    ----------\n    data : array_like\n        The input data.\n    axis : int, optional\n        The axis along which to detrend the data. By default this is the\n        last axis (-1).\n    type : {'linear', 'constant'}, optional\n        The type of detrending. If ``type == 'linear'`` (default),\n        the result of a linear least-squares fit to `data` is subtracted\n        from `data`.\n        If ``type == 'constant'``, only the mean of `data` is subtracted.\n    bp : array_like of ints, optional\n        A sequence of break points. If given, an individual linear fit is\n        performed for each part of `data` between two break points.\n        Break points are specified as indices into `data`.\n    overwrite_data : bool, optional\n        If True, perform in place detrending and avoid a copy. Default is False\n\n    Returns\n    -------\n    ret : ndarray\n        The detrended input data.\n\n    Examples\n    --------\n    >>> from scipy import signal\n    >>> randgen = np.random.RandomState(9)\n    >>> npoints = 1000\n    >>> noise = randgen.randn(npoints)\n    >>> x = 3 + 2*np.linspace(0, 1, npoints) + noise\n    >>> (signal.detrend(x) - noise).max() < 0.01\n    True\n\n    "
    if (type not in ['linear', 'l', 'constant', 'c']):
        raise ValueError("Trend type must be 'linear' or 'constant'.")
    data = np.asarray(data)
    dtype = data.dtype.char
    if (dtype not in 'dfDF'):
        dtype = 'd'
    if (type in ['constant', 'c']):
        ret = (data - np.expand_dims(np.mean(data, axis), axis))
        return ret
    else:
        dshape = data.shape
        N = dshape[axis]
        bp = np.sort(np.unique(np.r_[(0, bp, N)]))
        if np.any((bp > N)):
            raise ValueError('Breakpoints must be less than length of data along given axis.')
        Nreg = (len(bp) - 1)
        rnk = len(dshape)
        if (axis < 0):
            axis = (axis + rnk)
        newdims = np.r_[axis, 0:axis, (axis + 1):rnk]
        newdata = np.reshape(np.transpose(data, tuple(newdims)), (N, (_prod(dshape) // N)))
        if (not overwrite_data):
            newdata = newdata.copy()
        if (newdata.dtype.char not in 'dfDF'):
            newdata = newdata.astype(dtype)
        for m in range(Nreg):
            Npts = (bp[(m + 1)] - bp[m])
            A = np.ones((Npts, 2), dtype)
            A[:, 0] = np.cast[dtype](((np.arange(1, (Npts + 1)) * 1.0) / Npts))
            sl = slice(bp[m], bp[(m + 1)])
            (coef, resids, rank, s) = linalg.lstsq(A, newdata[sl])
            newdata[sl] = (newdata[sl] - np.dot(A, coef))
        tdshape = np.take(dshape, newdims, 0)
        ret = np.reshape(newdata, tuple(tdshape))
        vals = list(range(1, rnk))
        olddims = ((vals[:axis] + [0]) + vals[axis:])
        ret = np.transpose(ret, tuple(olddims))
        return ret