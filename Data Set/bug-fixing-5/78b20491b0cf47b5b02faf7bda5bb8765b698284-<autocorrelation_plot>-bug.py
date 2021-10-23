def autocorrelation_plot(series, ax=None, **kwds):
    '\n    Autocorrelation plot for time series.\n\n    Parameters\n    ----------\n    series : Time series\n    ax : Matplotlib axis object, optional\n    kwds : keywords\n        Options to pass to matplotlib plotting method\n\n    Returns\n    -------\n    class:`matplotlib.axis.Axes`\n    '
    plot_backend = _get_plot_backend('matplotlib')
    return plot_backend.autocorrelation_plot(series=series, ax=ax, **kwds)