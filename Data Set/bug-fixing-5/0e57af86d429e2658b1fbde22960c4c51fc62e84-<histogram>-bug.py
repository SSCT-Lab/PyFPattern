def histogram(a, bins=10, range=None, normed=False, weights=None, density=None):
    '\n    Compute the histogram of a set of data.\n\n    Parameters\n    ----------\n    a : array_like\n        Input data. The histogram is computed over the flattened array.\n    bins : int or sequence of scalars or str, optional\n        If `bins` is an int, it defines the number of equal-width\n        bins in the given range (10, by default). If `bins` is a\n        sequence, it defines the bin edges, including the rightmost\n        edge, allowing for non-uniform bin widths.\n\n        .. versionadded:: 1.11.0\n\n        If `bins` is a string from the list below, `histogram` will use\n        the method chosen to calculate the optimal bin width and\n        consequently the number of bins (see `Notes` for more detail on\n        the estimators) from the data that falls within the requested\n        range. While the bin width will be optimal for the actual data\n        in the range, the number of bins will be computed to fill the\n        entire range, including the empty portions. For visualisation,\n        using the \'auto\' option is suggested. Weighted data is not\n        supported for automated bin size selection.\n\n        \'auto\'\n            Maximum of the \'sturges\' and \'fd\' estimators. Provides good\n            all around performance.\n\n        \'fd\' (Freedman Diaconis Estimator)\n            Robust (resilient to outliers) estimator that takes into\n            account data variability and data size.\n\n        \'doane\'\n            An improved version of Sturges\' estimator that works better\n            with non-normal datasets.\n\n        \'scott\'\n            Less robust estimator that that takes into account data\n            variability and data size.\n\n        \'rice\'\n            Estimator does not take variability into account, only data\n            size. Commonly overestimates number of bins required.\n\n        \'sturges\'\n            R\'s default method, only accounts for data size. Only\n            optimal for gaussian data and underestimates number of bins\n            for large non-gaussian datasets.\n\n        \'sqrt\'\n            Square root (of data size) estimator, used by Excel and\n            other programs for its speed and simplicity.\n\n    range : (float, float), optional\n        The lower and upper range of the bins.  If not provided, range\n        is simply ``(a.min(), a.max())``.  Values outside the range are\n        ignored. The first element of the range must be less than or\n        equal to the second. `range` affects the automatic bin\n        computation as well. While bin width is computed to be optimal\n        based on the actual data within `range`, the bin count will fill\n        the entire range including portions containing no data.\n    normed : bool, optional\n        This keyword is deprecated in NumPy 1.6.0 due to confusing/buggy\n        behavior. It will be removed in NumPy 2.0.0. Use the ``density``\n        keyword instead. If ``False``, the result will contain the\n        number of samples in each bin. If ``True``, the result is the\n        value of the probability *density* function at the bin,\n        normalized such that the *integral* over the range is 1. Note\n        that this latter behavior is known to be buggy with unequal bin\n        widths; use ``density`` instead.\n    weights : array_like, optional\n        An array of weights, of the same shape as `a`.  Each value in\n        `a` only contributes its associated weight towards the bin count\n        (instead of 1). If `density` is True, the weights are\n        normalized, so that the integral of the density over the range\n        remains 1.\n    density : bool, optional\n        If ``False``, the result will contain the number of samples in\n        each bin. If ``True``, the result is the value of the\n        probability *density* function at the bin, normalized such that\n        the *integral* over the range is 1. Note that the sum of the\n        histogram values will not be equal to 1 unless bins of unity\n        width are chosen; it is not a probability *mass* function.\n\n        Overrides the ``normed`` keyword if given.\n\n    Returns\n    -------\n    hist : array\n        The values of the histogram. See `density` and `weights` for a\n        description of the possible semantics.\n    bin_edges : array of dtype float\n        Return the bin edges ``(length(hist)+1)``.\n\n\n    See Also\n    --------\n    histogramdd, bincount, searchsorted, digitize\n\n    Notes\n    -----\n    All but the last (righthand-most) bin is half-open.  In other words,\n    if `bins` is::\n\n      [1, 2, 3, 4]\n\n    then the first bin is ``[1, 2)`` (including 1, but excluding 2) and\n    the second ``[2, 3)``.  The last bin, however, is ``[3, 4]``, which\n    *includes* 4.\n\n    .. versionadded:: 1.11.0\n\n    The methods to estimate the optimal number of bins are well founded\n    in literature, and are inspired by the choices R provides for\n    histogram visualisation. Note that having the number of bins\n    proportional to :math:`n^{1/3}` is asymptotically optimal, which is\n    why it appears in most estimators. These are simply plug-in methods\n    that give good starting points for number of bins. In the equations\n    below, :math:`h` is the binwidth and :math:`n_h` is the number of\n    bins. All estimators that compute bin counts are recast to bin width\n    using the `ptp` of the data. The final bin count is obtained from\n    ``np.round(np.ceil(range / h))`.\n\n    \'Auto\' (maximum of the \'Sturges\' and \'FD\' estimators)\n        A compromise to get a good value. For small datasets the Sturges\n        value will usually be chosen, while larger datasets will usually\n        default to FD.  Avoids the overly conservative behaviour of FD\n        and Sturges for small and large datasets respectively.\n        Switchover point is usually :math:`a.size \\approx 1000`.\n\n    \'FD\' (Freedman Diaconis Estimator)\n        .. math:: h = 2 \\frac{IQR}{n^{1/3}}\n\n        The binwidth is proportional to the interquartile range (IQR)\n        and inversely proportional to cube root of a.size. Can be too\n        conservative for small datasets, but is quite good for large\n        datasets. The IQR is very robust to outliers.\n\n    \'Scott\'\n        .. math:: h = \\sigma \\sqrt[3]{\\frac{24 * \\sqrt{\\pi}}{n}}\n\n        The binwidth is proportional to the standard deviation of the\n        data and inversely proportional to cube root of ``x.size``. Can\n        be too conservative for small datasets, but is quite good for\n        large datasets. The standard deviation is not very robust to\n        outliers. Values are very similar to the Freedman-Diaconis\n        estimator in the absence of outliers.\n\n    \'Rice\'\n        .. math:: n_h = 2n^{1/3}\n\n        The number of bins is only proportional to cube root of\n        ``a.size``. It tends to overestimate the number of bins and it\n        does not take into account data variability.\n\n    \'Sturges\'\n        .. math:: n_h = \\log _{2}n+1\n\n        The number of bins is the base 2 log of ``a.size``.  This\n        estimator assumes normality of data and is too conservative for\n        larger, non-normal datasets. This is the default method in R\'s\n        ``hist`` method.\n\n    \'Doane\'\n        .. math:: n_h = 1 + \\log_{2}(n) +\n                        \\log_{2}(1 + \\frac{|g_1|}{\\sigma_{g_1}})\n\n            g_1 = mean[(\\frac{x - \\mu}{\\sigma})^3]\n\n            \\sigma_{g_1} = \\sqrt{\\frac{6(n - 2)}{(n + 1)(n + 3)}}\n\n        An improved version of Sturges\' formula that produces better\n        estimates for non-normal datasets. This estimator attempts to\n        account for the skew of the data.\n\n    \'Sqrt\'\n        .. math:: n_h = \\sqrt n\n        The simplest and fastest estimator. Only takes into account the\n        data size.\n\n    Examples\n    --------\n    >>> np.histogram([1, 2, 1], bins=[0, 1, 2, 3])\n    (array([0, 2, 1]), array([0, 1, 2, 3]))\n    >>> np.histogram(np.arange(4), bins=np.arange(5), density=True)\n    (array([ 0.25,  0.25,  0.25,  0.25]), array([0, 1, 2, 3, 4]))\n    >>> np.histogram([[1, 2, 1], [1, 0, 1]], bins=[0,1,2,3])\n    (array([1, 4, 1]), array([0, 1, 2, 3]))\n\n    >>> a = np.arange(5)\n    >>> hist, bin_edges = np.histogram(a, density=True)\n    >>> hist\n    array([ 0.5,  0. ,  0.5,  0. ,  0. ,  0.5,  0. ,  0.5,  0. ,  0.5])\n    >>> hist.sum()\n    2.4999999999999996\n    >>> np.sum(hist * np.diff(bin_edges))\n    1.0\n\n    .. versionadded:: 1.11.0\n\n    Automated Bin Selection Methods example, using 2 peak random data\n    with 2000 points:\n\n    >>> import matplotlib.pyplot as plt\n    >>> rng = np.random.RandomState(10)  # deterministic random data\n    >>> a = np.hstack((rng.normal(size=1000),\n    ...                rng.normal(loc=5, scale=2, size=1000)))\n    >>> plt.hist(a, bins=\'auto\')  # arguments are passed to np.histogram\n    >>> plt.title("Histogram with \'auto\' bins")\n    >>> plt.show()\n\n    '
    a = np.asarray(a)
    if (weights is not None):
        weights = np.asarray(weights)
        if (weights.shape != a.shape):
            raise ValueError('weights should have the same shape as a.')
        weights = weights.ravel()
    a = a.ravel()
    if (range is None):
        if (a.size == 0):
            (first_edge, last_edge) = (0.0, 1.0)
        else:
            (first_edge, last_edge) = ((a.min() + 0.0), (a.max() + 0.0))
    else:
        (first_edge, last_edge) = [(mi + 0.0) for mi in range]
    if (first_edge > last_edge):
        raise ValueError('max must be larger than min in range parameter.')
    if (not np.all(np.isfinite([first_edge, last_edge]))):
        raise ValueError('range parameter must be finite.')
    if (first_edge == last_edge):
        first_edge -= 0.5
        last_edge += 0.5
    if (density is not None):
        normed = False
    n_equal_bins = None
    bin_edges = None
    if isinstance(bins, basestring):
        bin_name = bins
        if (bin_name not in _hist_bin_selectors):
            raise ValueError('{!r} is not a valid estimator for `bins`'.format(bin_name))
        if (weights is not None):
            raise TypeError('Automated estimation of the number of bins is not supported for weighted data')
        b = a
        if (range is not None):
            keep = (a >= first_edge)
            keep &= (a <= last_edge)
            if (not np.logical_and.reduce(keep)):
                b = a[keep]
        if (b.size == 0):
            n_equal_bins = 1
        else:
            width = _hist_bin_selectors[bin_name](b)
            if width:
                n_equal_bins = int(np.ceil(((last_edge - first_edge) / width)))
            else:
                n_equal_bins = 1
    elif (np.ndim(bins) == 0):
        try:
            n_equal_bins = operator.index(bins)
        except TypeError:
            raise TypeError('`bins` must be an integer, a string, or an array')
        if (n_equal_bins < 1):
            raise ValueError('`bins` must be positive, when an integer')
    elif (np.ndim(bins) == 1):
        bin_edges = np.asarray(bins)
        if np.any((bin_edges[:(- 1)] > bin_edges[1:])):
            raise ValueError('`bins` must increase monotonically, when an array')
    else:
        raise ValueError('`bins` must be 1d, when an array')
    del bins
    if (n_equal_bins is not None):
        bin_edges = np.linspace(first_edge, last_edge, (n_equal_bins + 1), endpoint=True)
    if (weights is None):
        ntype = np.dtype(np.intp)
    else:
        ntype = weights.dtype
    BLOCK = 65536
    simple_weights = ((weights is None) or np.can_cast(weights.dtype, np.double) or np.can_cast(weights.dtype, complex))
    if ((n_equal_bins is not None) and simple_weights):
        n = np.zeros(n_equal_bins, ntype)
        norm = (n_equal_bins / (last_edge - first_edge))
        for i in np.arange(0, len(a), BLOCK):
            tmp_a = a[i:(i + BLOCK)]
            if (weights is None):
                tmp_w = None
            else:
                tmp_w = weights[i:(i + BLOCK)]
            keep = (tmp_a >= first_edge)
            keep &= (tmp_a <= last_edge)
            if (not np.logical_and.reduce(keep)):
                tmp_a = tmp_a[keep]
                if (tmp_w is not None):
                    tmp_w = tmp_w[keep]
            tmp_a_data = tmp_a.astype(float)
            tmp_a = (tmp_a_data - first_edge)
            tmp_a *= norm
            indices = tmp_a.astype(np.intp)
            indices[(indices == n_equal_bins)] -= 1
            decrement = (tmp_a_data < bin_edges[indices])
            indices[decrement] -= 1
            increment = ((tmp_a_data >= bin_edges[(indices + 1)]) & (indices != (n_equal_bins - 1)))
            indices[increment] += 1
            if (ntype.kind == 'c'):
                n.real += np.bincount(indices, weights=tmp_w.real, minlength=n_equal_bins)
                n.imag += np.bincount(indices, weights=tmp_w.imag, minlength=n_equal_bins)
            else:
                n += np.bincount(indices, weights=tmp_w, minlength=n_equal_bins).astype(ntype)
    else:
        cum_n = np.zeros(bin_edges.shape, ntype)
        if (weights is None):
            for i in np.arange(0, len(a), BLOCK):
                sa = np.sort(a[i:(i + BLOCK)])
                cum_n += np.r_[(sa.searchsorted(bin_edges[:(- 1)], 'left'), sa.searchsorted(bin_edges[(- 1)], 'right'))]
        else:
            zero = np.array(0, dtype=ntype)
            for i in np.arange(0, len(a), BLOCK):
                tmp_a = a[i:(i + BLOCK)]
                tmp_w = weights[i:(i + BLOCK)]
                sorting_index = np.argsort(tmp_a)
                sa = tmp_a[sorting_index]
                sw = tmp_w[sorting_index]
                cw = np.concatenate(([zero], sw.cumsum()))
                bin_index = np.r_[(sa.searchsorted(bin_edges[:(- 1)], 'left'), sa.searchsorted(bin_edges[(- 1)], 'right'))]
                cum_n += cw[bin_index]
        n = np.diff(cum_n)
    if density:
        db = np.array(np.diff(bin_edges), float)
        return (((n / db) / n.sum()), bin_edges)
    elif normed:
        db = np.array(np.diff(bin_edges), float)
        return ((n / (n * db).sum()), bin_edges)
    else:
        return (n, bin_edges)