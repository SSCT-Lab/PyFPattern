def binned_statistic_dd(sample, values, statistic='mean', bins=10, range=None, expand_binnumbers=False):
    "\n    Compute a multidimensional binned statistic for a set of data.\n\n    This is a generalization of a histogramdd function.  A histogram divides\n    the space into bins, and returns the count of the number of points in\n    each bin.  This function allows the computation of the sum, mean, median,\n    or other statistic of the values within each bin.\n\n    Parameters\n    ----------\n    sample : array_like\n        Data to histogram passed as a sequence of N arrays of length D, or\n        as an (N,D) array.\n    values : (N,) array_like or list of (N,) array_like\n        The data on which the statistic will be computed.  This must be\n        the same shape as `sample`, or a list of sequences - each with the\n        same shape as `sample`.  If `values` is such a list, the statistic\n        will be computed on each independently.\n    statistic : string or callable, optional\n        The statistic to compute (default is 'mean').\n        The following statistics are available:\n\n          * 'mean' : compute the mean of values for points within each bin.\n            Empty bins will be represented by NaN.\n          * 'median' : compute the median of values for points within each\n            bin. Empty bins will be represented by NaN.\n          * 'count' : compute the count of points within each bin.  This is\n            identical to an unweighted histogram.  `values` array is not\n            referenced.\n          * 'sum' : compute the sum of values for points within each bin.\n            This is identical to a weighted histogram.\n          * 'std' : compute the standard deviation within each bin. This\n            is implicitly calculated with ddof=0.\n          * 'min' : compute the minimum of values for points within each bin.\n            Empty bins will be represented by NaN.\n          * 'max' : compute the maximum of values for point within each bin.\n            Empty bins will be represented by NaN.\n          * function : a user-defined function which takes a 1D array of\n            values, and outputs a single numerical statistic. This function\n            will be called on the values in each bin.  Empty bins will be\n            represented by function([]), or NaN if this returns an error.\n\n    bins : sequence or int, optional\n        The bin specification must be in one of the following forms:\n\n          * A sequence of arrays describing the bin edges along each dimension.\n          * The number of bins for each dimension (nx, ny, ... = bins).\n          * The number of bins for all dimensions (nx = ny = ... = bins).\n\n    range : sequence, optional\n        A sequence of lower and upper bin edges to be used if the edges are\n        not given explicitly in `bins`. Defaults to the minimum and maximum\n        values along each dimension.\n    expand_binnumbers : bool, optional\n        'False' (default): the returned `binnumber` is a shape (N,) array of\n        linearized bin indices.\n        'True': the returned `binnumber` is 'unraveled' into a shape (D,N)\n        ndarray, where each row gives the bin numbers in the corresponding\n        dimension.\n        See the `binnumber` returned value, and the `Examples` section of\n        `binned_statistic_2d`.\n\n        .. versionadded:: 0.17.0\n\n    Returns\n    -------\n    statistic : ndarray, shape(nx1, nx2, nx3,...)\n        The values of the selected statistic in each two-dimensional bin.\n    bin_edges : list of ndarrays\n        A list of D arrays describing the (nxi + 1) bin edges for each\n        dimension.\n    binnumber : (N,) array of ints or (D,N) ndarray of ints\n        This assigns to each element of `sample` an integer that represents the\n        bin in which this observation falls.  The representation depends on the\n        `expand_binnumbers` argument.  See `Notes` for details.\n\n\n    See Also\n    --------\n    numpy.digitize, numpy.histogramdd, binned_statistic, binned_statistic_2d\n\n    Notes\n    -----\n    Binedges:\n    All but the last (righthand-most) bin is half-open in each dimension.  In\n    other words, if `bins` is ``[1, 2, 3, 4]``, then the first bin is\n    ``[1, 2)`` (including 1, but excluding 2) and the second ``[2, 3)``.  The\n    last bin, however, is ``[3, 4]``, which *includes* 4.\n\n    `binnumber`:\n    This returned argument assigns to each element of `sample` an integer that\n    represents the bin in which it belongs.  The representation depends on the\n    `expand_binnumbers` argument. If 'False' (default): The returned\n    `binnumber` is a shape (N,) array of linearized indices mapping each\n    element of `sample` to its corresponding bin (using row-major ordering).\n    If 'True': The returned `binnumber` is a shape (D,N) ndarray where\n    each row indicates bin placements for each dimension respectively.  In each\n    dimension, a binnumber of `i` means the corresponding value is between\n    (bin_edges[D][i-1], bin_edges[D][i]), for each dimension 'D'.\n\n    .. versionadded:: 0.11.0\n\n    Examples\n    --------\n    >>> from scipy import stats\n    >>> import matplotlib.pyplot as plt\n    >>> from mpl_toolkits.mplot3d import Axes3D\n\n    Take an array of 600 (x, y) coordinates as an example.\n    `binned_statistic_dd` can handle arrays of higher dimension `D`. But a plot\n    of dimension `D+1` is required.\n\n    >>> mu = np.array([0., 1.])\n    >>> sigma = np.array([[1., -0.5],[-0.5, 1.5]])\n    >>> multinormal = stats.multivariate_normal(mu, sigma)\n    >>> data = multinormal.rvs(size=600, random_state=235412)\n    >>> data.shape\n    (600, 2)\n\n    Create bins and count how many arrays fall in each bin:\n\n    >>> N = 60\n    >>> x = np.linspace(-3, 3, N)\n    >>> y = np.linspace(-3, 4, N)\n    >>> ret = stats.binned_statistic_dd(data, np.arange(600), bins=[x, y],\n    ...                                 statistic='count')\n    >>> bincounts = ret.statistic\n\n    Set the volume and the location of bars:\n\n    >>> dx = x[1] - x[0]\n    >>> dy = y[1] - y[0]\n    >>> x, y = np.meshgrid(x[:-1]+dx/2, y[:-1]+dy/2)\n    >>> z = 0\n\n    >>> bincounts = bincounts.ravel()\n    >>> x = x.ravel()\n    >>> y = y.ravel()\n\n    >>> fig = plt.figure()\n    >>> ax = fig.add_subplot(111, projection='3d')\n    >>> with np.errstate(divide='ignore'):   # silence random axes3d warning\n    ...     ax.bar3d(x, y, z, dx, dy, bincounts)\n\n    "
    known_stats = ['mean', 'median', 'count', 'sum', 'std', 'min', 'max']
    if ((not callable(statistic)) and (statistic not in known_stats)):
        raise ValueError(('invalid statistic %r' % (statistic,)))
    try:
        (Dlen, Ndim) = sample.shape
    except (AttributeError, ValueError):
        sample = np.atleast_2d(sample).T
        (Dlen, Ndim) = sample.shape
    values = np.asarray(values)
    input_shape = list(values.shape)
    values = np.atleast_2d(values)
    (Vdim, Vlen) = values.shape
    if ((statistic != 'count') and (Vlen != Dlen)):
        raise AttributeError('The number of `values` elements must match the length of each `sample` dimension.')
    nbin = np.empty(Ndim, int)
    edges = (Ndim * [None])
    dedges = (Ndim * [None])
    try:
        M = len(bins)
        if (M != Ndim):
            raise AttributeError('The dimension of bins must be equal to the dimension of the sample x.')
    except TypeError:
        bins = (Ndim * [bins])
    if (range is None):
        smin = np.atleast_1d(np.array(sample.min(axis=0), float))
        smax = np.atleast_1d(np.array(sample.max(axis=0), float))
    else:
        smin = np.zeros(Ndim)
        smax = np.zeros(Ndim)
        for i in xrange(Ndim):
            (smin[i], smax[i]) = range[i]
    for i in xrange(len(smin)):
        if (smin[i] == smax[i]):
            smin[i] = (smin[i] - 0.5)
            smax[i] = (smax[i] + 0.5)
    for i in xrange(Ndim):
        if np.isscalar(bins[i]):
            nbin[i] = (bins[i] + 2)
            edges[i] = np.linspace(smin[i], smax[i], (nbin[i] - 1))
        else:
            edges[i] = np.asarray(bins[i], float)
            nbin[i] = (len(edges[i]) + 1)
        dedges[i] = np.diff(edges[i])
    nbin = np.asarray(nbin)
    sampBin = [np.digitize(sample[:, i], edges[i]) for i in xrange(Ndim)]
    for i in xrange(Ndim):
        decimal = (int((- np.log10(dedges[i].min()))) + 6)
        on_edge = np.where((np.around(sample[:, i], decimal) == np.around(edges[i][(- 1)], decimal)))[0]
        sampBin[i][on_edge] -= 1
    binnumbers = np.ravel_multi_index(sampBin, nbin)
    result = np.empty([Vdim, nbin.prod()], float)
    if (statistic == 'mean'):
        result.fill(np.nan)
        flatcount = np.bincount(binnumbers, None)
        a = flatcount.nonzero()
        for vv in xrange(Vdim):
            flatsum = np.bincount(binnumbers, values[vv])
            result[(vv, a)] = (flatsum[a] / flatcount[a])
    elif (statistic == 'std'):
        result.fill(0)
        flatcount = np.bincount(binnumbers, None)
        a = flatcount.nonzero()
        for i in np.unique(binnumbers):
            for vv in xrange(Vdim):
                result[(vv, i)] = np.std(values[(vv, (binnumbers == i))])
    elif (statistic == 'count'):
        result.fill(0)
        flatcount = np.bincount(binnumbers, None)
        a = np.arange(len(flatcount))
        result[:, a] = flatcount[np.newaxis, :]
    elif (statistic == 'sum'):
        result.fill(0)
        for vv in xrange(Vdim):
            flatsum = np.bincount(binnumbers, values[vv])
            a = np.arange(len(flatsum))
            result[(vv, a)] = flatsum
    elif (statistic == 'median'):
        result.fill(np.nan)
        for i in np.unique(binnumbers):
            for vv in xrange(Vdim):
                result[(vv, i)] = np.median(values[(vv, (binnumbers == i))])
    elif (statistic == 'min'):
        result.fill(np.nan)
        for i in np.unique(binnumbers):
            for vv in xrange(Vdim):
                result[(vv, i)] = np.min(values[(vv, (binnumbers == i))])
    elif (statistic == 'max'):
        result.fill(np.nan)
        for i in np.unique(binnumbers):
            for vv in xrange(Vdim):
                result[(vv, i)] = np.max(values[(vv, (binnumbers == i))])
    elif callable(statistic):
        with np.errstate(invalid='ignore'), suppress_warnings() as sup:
            sup.filter(RuntimeWarning)
            try:
                null = statistic([])
            except Exception:
                null = np.nan
        result.fill(null)
        for i in np.unique(binnumbers):
            for vv in xrange(Vdim):
                result[(vv, i)] = statistic(values[(vv, (binnumbers == i))])
    result = result.reshape(np.append(Vdim, nbin))
    core = tuple(([slice(None)] + (Ndim * [slice(1, (- 1))])))
    result = result[core]
    if (expand_binnumbers and (Ndim > 1)):
        binnumbers = np.asarray(np.unravel_index(binnumbers, nbin))
    if np.any((result.shape[1:] != (nbin - 2))):
        raise RuntimeError('Internal Shape Error')
    result = result.reshape((input_shape[:(- 1)] + list((nbin - 2))))
    return BinnedStatisticddResult(result, edges, binnumbers)