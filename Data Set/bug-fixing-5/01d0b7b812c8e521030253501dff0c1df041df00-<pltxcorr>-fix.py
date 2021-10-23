def pltxcorr(self, x, y, normed=True, detrend=detrend_none, usevlines=True, maxlags=10, **kwargs):
    "\n    call signature::\n\n        def xcorr(self, x, y, normed=True, detrend=detrend_none,\n          usevlines=True, maxlags=10, **kwargs):\n\n    Plot the cross correlation between *x* and *y*.  If *normed* =\n    *True*, normalize the data by the cross correlation at 0-th\n    lag.  *x* and y are detrended by the *detrend* callable\n    (default no normalization).  *x* and *y* must be equal length.\n\n    Data are plotted as ``plot(lags, c, **kwargs)``\n\n    Return value is a tuple (*lags*, *c*, *line*) where:\n\n      - *lags* are a length ``2*maxlags+1`` lag vector\n\n      - *c* is the ``2*maxlags+1`` auto correlation vector\n\n      - *line* is a :class:`~matplotlib.lines.Line2D` instance\n         returned by :func:`~matplotlib.pyplot.plot`.\n\n    The default *linestyle* is *None* and the default *marker* is\n    'o', though these can be overridden with keyword args.  The\n    cross correlation is performed with :func:`numpy.correlate`\n    with *mode* = 2.\n\n    If *usevlines* is *True*:\n\n       :func:`~matplotlib.pyplot.vlines`\n       rather than :func:`~matplotlib.pyplot.plot` is used to draw\n       vertical lines from the origin to the xcorr.  Otherwise the\n       plotstyle is determined by the kwargs, which are\n       :class:`~matplotlib.lines.Line2D` properties.\n\n       The return value is a tuple (*lags*, *c*, *linecol*, *b*)\n       where *linecol* is the\n       :class:`matplotlib.collections.LineCollection` instance and\n       *b* is the *x*-axis.\n\n    *maxlags* is a positive integer detailing the number of lags to show.\n    The default value of *None* will return all ``(2*len(x)-1)`` lags.\n\n    **Example:**\n\n    :func:`~matplotlib.pyplot.xcorr` above, and\n    :func:`~matplotlib.pyplot.acorr` below.\n\n    **Example:**\n\n    .. plot:: mpl_examples/pylab_examples/xcorr_demo.py\n    "
    Nx = len(x)
    if (Nx != len(y)):
        raise ValueError('x and y must be equal length')
    x = detrend(np.asarray(x))
    y = detrend(np.asarray(y))
    c = np.correlate(x, y, mode=2)
    if normed:
        c /= np.sqrt((np.dot(x, x) * np.dot(y, y)))
    if (maxlags is None):
        maxlags = (Nx - 1)
    if ((maxlags >= Nx) or (maxlags < 1)):
        raise ValueError(('maxlags must be None or strictly positive < %d' % Nx))
    lags = np.arange((- maxlags), (maxlags + 1))
    c = c[((Nx - 1) - maxlags):(Nx + maxlags)]
    if usevlines:
        a = self.vlines(lags, [0], c, **kwargs)
        b = self.axhline(**kwargs)
        kwargs.setdefault('marker', 'o')
        kwargs.setdefault('linestyle', 'None')
        d = self.plot(lags, c, **kwargs)
    else:
        kwargs.setdefault('marker', 'o')
        kwargs.setdefault('linestyle', 'None')
        (a,) = self.plot(lags, c, **kwargs)
        b = None
    return (lags, c, a, b)