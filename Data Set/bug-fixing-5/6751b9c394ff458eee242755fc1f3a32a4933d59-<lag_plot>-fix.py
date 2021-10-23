def lag_plot(series, lag=1, ax=None, **kwds):
    'Lag plot for time series.\n\n    Parameters\n    ----------\n    series: Time series\n    lag: lag of the scatter plot, default 1\n    ax: Matplotlib axis object, optional\n    kwds: Matplotlib scatter method keyword arguments, optional\n\n    Returns\n    -------\n    ax: Matplotlib axis object\n    '
    import matplotlib.pyplot as plt
    kwds.setdefault('c', plt.rcParams['patch.facecolor'])
    data = series.values
    y1 = data[:(- lag)]
    y2 = data[lag:]
    if (ax is None):
        ax = plt.gca()
    ax.set_xlabel('y(t)')
    ax.set_ylabel('y(t + {lag})'.format(lag=lag))
    ax.scatter(y1, y2, **kwds)
    return ax