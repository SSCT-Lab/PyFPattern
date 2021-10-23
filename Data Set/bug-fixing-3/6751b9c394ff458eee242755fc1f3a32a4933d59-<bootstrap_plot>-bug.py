def bootstrap_plot(series, fig=None, size=50, samples=500, **kwds):
    'Bootstrap plot.\n\n    Parameters:\n    -----------\n    series: Time series\n    fig: matplotlib figure object, optional\n    size: number of data points to consider during each sampling\n    samples: number of times the bootstrap procedure is performed\n    kwds: optional keyword arguments for plotting commands, must be accepted\n        by both hist and plot\n\n    Returns:\n    --------\n    fig: matplotlib figure\n    '
    import random
    import matplotlib.pyplot as plt
    data = list(series.values)
    samplings = [random.sample(data, size) for _ in range(samples)]
    means = np.array([np.mean(sampling) for sampling in samplings])
    medians = np.array([np.median(sampling) for sampling in samplings])
    midranges = np.array([((min(sampling) + max(sampling)) * 0.5) for sampling in samplings])
    if (fig is None):
        fig = plt.figure()
    x = lrange(samples)
    axes = []
    ax1 = fig.add_subplot(2, 3, 1)
    ax1.set_xlabel('Sample')
    axes.append(ax1)
    ax1.plot(x, means, **kwds)
    ax2 = fig.add_subplot(2, 3, 2)
    ax2.set_xlabel('Sample')
    axes.append(ax2)
    ax2.plot(x, medians, **kwds)
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.set_xlabel('Sample')
    axes.append(ax3)
    ax3.plot(x, midranges, **kwds)
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.set_xlabel('Mean')
    axes.append(ax4)
    ax4.hist(means, **kwds)
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.set_xlabel('Median')
    axes.append(ax5)
    ax5.hist(medians, **kwds)
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.set_xlabel('Midrange')
    axes.append(ax6)
    ax6.hist(midranges, **kwds)
    for axis in axes:
        plt.setp(axis.get_xticklabels(), fontsize=8)
        plt.setp(axis.get_yticklabels(), fontsize=8)
    return fig