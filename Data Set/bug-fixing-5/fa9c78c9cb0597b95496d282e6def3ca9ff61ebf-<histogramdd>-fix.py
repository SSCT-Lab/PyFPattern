def histogramdd(sample, bins=10, range=None, normed=False, weights=None):
    '\n    Compute the multidimensional histogram of some data.\n\n    Parameters\n    ----------\n    sample : (N, D) array, or (D, N) array_like\n        The data to be histogrammed.\n\n        Note the unusual interpretation of sample when an array_like:\n\n        * When an array, each row is a coordinate in a D-dimensional space -\n          such as ``histogramgramdd(np.array([p1, p2, p3]))``.\n        * When an array_like, each element is the list of values for single\n          coordinate - such as ``histogramgramdd((X, Y, Z))``.\n\n        The first form should be preferred.\n\n    bins : sequence or int, optional\n        The bin specification:\n\n        * A sequence of arrays describing the bin edges along each dimension.\n        * The number of bins for each dimension (nx, ny, ... =bins)\n        * The number of bins for all dimensions (nx=ny=...=bins).\n\n    range : sequence, optional\n        A sequence of length D, each an optional (lower, upper) tuple giving\n        the outer bin edges to be used if the edges are not given explicitly in\n        `bins`.\n        An entry of None in the sequence results in the minimum and maximum\n        values being used for the corresponding dimension.\n        The default, None, is equivalent to passing a tuple of D None values.\n    normed : bool, optional\n        If False, returns the number of samples in each bin. If True,\n        returns the bin density ``bin_count / sample_count / bin_volume``.\n    weights : (N,) array_like, optional\n        An array of values `w_i` weighing each sample `(x_i, y_i, z_i, ...)`.\n        Weights are normalized to 1 if normed is True. If normed is False,\n        the values of the returned histogram are equal to the sum of the\n        weights belonging to the samples falling into each bin.\n\n    Returns\n    -------\n    H : ndarray\n        The multidimensional histogram of sample x. See normed and weights\n        for the different possible semantics.\n    edges : list\n        A list of D arrays describing the bin edges for each dimension.\n\n    See Also\n    --------\n    histogram: 1-D histogram\n    histogram2d: 2-D histogram\n\n    Examples\n    --------\n    >>> r = np.random.randn(100,3)\n    >>> H, edges = np.histogramdd(r, bins = (5, 8, 4))\n    >>> H.shape, edges[0].size, edges[1].size, edges[2].size\n    ((5, 8, 4), 6, 9, 5)\n\n    '
    try:
        (N, D) = sample.shape
    except (AttributeError, ValueError):
        sample = np.atleast_2d(sample).T
        (N, D) = sample.shape
    nbin = np.empty(D, int)
    edges = (D * [None])
    dedges = (D * [None])
    if (weights is not None):
        weights = np.asarray(weights)
    try:
        M = len(bins)
        if (M != D):
            raise ValueError('The dimension of bins must be equal to the dimension of the  sample x.')
    except TypeError:
        bins = (D * [bins])
    if np.issubdtype(sample.dtype, np.inexact):
        edge_dt = sample.dtype
    else:
        edge_dt = float
    if (range is None):
        range = ((None,) * D)
    elif (len(range) != D):
        raise ValueError('range argument must have one entry per dimension')
    for i in _range(D):
        if (np.ndim(bins[i]) == 0):
            if (bins[i] < 1):
                raise ValueError('`bins[{}]` must be positive, when an integer'.format(i))
            (smin, smax) = _get_outer_edges(sample[:, i], range[i])
            edges[i] = np.linspace(smin, smax, (bins[i] + 1), dtype=edge_dt)
        elif (np.ndim(bins[i]) == 1):
            edges[i] = np.asarray(bins[i], edge_dt)
            if np.any((edges[i][:(- 1)] >= edges[i][1:])):
                raise ValueError('`bins[{}]` must be strictly increasing, when an array'.format(i))
        else:
            raise ValueError('`bins[{}]` must be a scalar or 1d array'.format(i))
        nbin[i] = (len(edges[i]) + 1)
        dedges[i] = np.diff(edges[i])
    Ncount = tuple((np.digitize(sample[:, i], edges[i]) for i in _range(D)))
    for i in _range(D):
        mindiff = dedges[i].min()
        if (not np.isinf(mindiff)):
            decimal = (int((- np.log10(mindiff))) + 6)
            not_smaller_than_edge = (sample[:, i] >= edges[i][(- 1)])
            on_edge = (np.around(sample[:, i], decimal) == np.around(edges[i][(- 1)], decimal))
            Ncount[i][(on_edge & not_smaller_than_edge)] -= 1
    xy = np.ravel_multi_index(Ncount, nbin)
    hist = np.bincount(xy, weights, minlength=nbin.prod())
    hist = hist.reshape(nbin)
    hist = hist.astype(float, casting='safe')
    core = (D * (slice(1, (- 1)),))
    hist = hist[core]
    if normed:
        s = hist.sum()
        for i in _range(D):
            shape = np.ones(D, int)
            shape[i] = (nbin[i] - 2)
            hist = (hist / dedges[i].reshape(shape))
        hist /= s
    if (hist.shape != (nbin - 2)).any():
        raise RuntimeError('Internal Shape Error')
    return (hist, edges)