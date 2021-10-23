

def plot_partial_dependence(gbrt, X, features, feature_names=None, label=None, n_cols=3, grid_resolution=100, percentiles=(0.05, 0.95), n_jobs=1, verbose=0, ax=None, line_kw=None, contour_kw=None, **fig_kw):
    "Partial dependence plots for ``features``.\n\n    The ``len(features)`` plots are arranged in a grid with ``n_cols``\n    columns. Two-way partial dependence plots are plotted as contour\n    plots.\n\n    Read more in the :ref:`User Guide <partial_dependence>`.\n\n    Parameters\n    ----------\n    gbrt : BaseGradientBoosting\n        A fitted gradient boosting model.\n    X : array-like, shape=(n_samples, n_features)\n        The data on which ``gbrt`` was trained.\n    features : seq of tuples or ints\n        If seq[i] is an int or a tuple with one int value, a one-way\n        PDP is created; if seq[i] is a tuple of two ints, a two-way\n        PDP is created.\n    feature_names : seq of str\n        Name of each feature; feature_names[i] holds\n        the name of the feature with index i.\n    label : object\n        The class label for which the PDPs should be computed.\n        Only if gbrt is a multi-class model. Must be in ``gbrt.classes_``.\n    n_cols : int\n        The number of columns in the grid plot (default: 3).\n    percentiles : (low, high), default=(0.05, 0.95)\n        The lower and upper percentile used to create the extreme values\n        for the PDP axes.\n    grid_resolution : int, default=100\n        The number of equally spaced points on the axes.\n    n_jobs : int\n        The number of CPUs to use to compute the PDs. -1 means 'all CPUs'.\n        Defaults to 1.\n    verbose : int\n        Verbose output during PD computations. Defaults to 0.\n    ax : Matplotlib axis object, default None\n        An axis object onto which the plots will be drawn.\n    line_kw : dict\n        Dict with keywords passed to the ``matplotlib.pyplot.plot`` call.\n        For one-way partial dependence plots.\n    contour_kw : dict\n        Dict with keywords passed to the ``matplotlib.pyplot.plot`` call.\n        For two-way partial dependence plots.\n    fig_kw : dict\n        Dict with keywords passed to the figure() call.\n        Note that all keywords not recognized above will be automatically\n        included here.\n\n    Returns\n    -------\n    fig : figure\n        The Matplotlib Figure object.\n    axs : seq of Axis objects\n        A seq of Axis objects, one for each subplot.\n\n    Examples\n    --------\n    >>> from sklearn.datasets import make_friedman1\n    >>> from sklearn.ensemble import GradientBoostingRegressor\n    >>> X, y = make_friedman1()\n    >>> clf = GradientBoostingRegressor(n_estimators=10).fit(X, y)\n    >>> fig, axs = plot_partial_dependence(clf, X, [0, (0, 1)]) #doctest: +SKIP\n    ...\n    "
    import matplotlib.pyplot as plt
    from matplotlib import transforms
    from matplotlib.ticker import MaxNLocator
    from matplotlib.ticker import ScalarFormatter
    if (not isinstance(gbrt, BaseGradientBoosting)):
        raise ValueError('gbrt has to be an instance of BaseGradientBoosting')
    if (gbrt.estimators_.shape[0] == 0):
        raise ValueError(('Call %s.fit before partial_dependence' % gbrt.__class__.__name__))
    if (hasattr(gbrt, 'classes_') and (np.size(gbrt.classes_) > 2)):
        if (label is None):
            raise ValueError('label is not given for multi-class PDP')
        label_idx = np.searchsorted(gbrt.classes_, label)
        if (gbrt.classes_[label_idx] != label):
            raise ValueError(('label %s not in ``gbrt.classes_``' % str(label)))
    else:
        label_idx = 0
    X = check_array(X, dtype=DTYPE, order='C')
    if (gbrt.n_features != X.shape[1]):
        raise ValueError('X.shape[1] does not match gbrt.n_features')
    if (line_kw is None):
        line_kw = {
            'color': 'green',
        }
    if (contour_kw is None):
        contour_kw = {
            
        }
    if (feature_names is None):
        feature_names = [str(i) for i in range(gbrt.n_features)]
    elif isinstance(feature_names, np.ndarray):
        feature_names = feature_names.tolist()

    def convert_feature(fx):
        if isinstance(fx, six.string_types):
            try:
                fx = feature_names.index(fx)
            except ValueError:
                raise ValueError(('Feature %s not in feature_names' % fx))
        return fx
    tmp_features = []
    for fxs in features:
        if isinstance(fxs, ((numbers.Integral,) + six.string_types)):
            fxs = (fxs,)
        try:
            fxs = np.array([convert_feature(fx) for fx in fxs], dtype=np.int32)
        except TypeError:
            raise ValueError('features must be either int, str, or tuple of int/str')
        if (not (1 <= np.size(fxs) <= 2)):
            raise ValueError('target features must be either one or two')
        tmp_features.append(fxs)
    features = tmp_features
    names = []
    try:
        for fxs in features:
            l = []
            for i in fxs:
                l.append(feature_names[i])
            names.append(l)
    except IndexError:
        raise ValueError(('features[i] must be in [0, n_features) but was %d' % i))
    pd_result = Parallel(n_jobs=n_jobs, verbose=verbose)((delayed(partial_dependence)(gbrt, fxs, X=X, grid_resolution=grid_resolution, percentiles=percentiles) for fxs in features))
    pdp_lim = {
        
    }
    for (pdp, axes) in pd_result:
        (min_pd, max_pd) = (pdp[label_idx].min(), pdp[label_idx].max())
        n_fx = len(axes)
        (old_min_pd, old_max_pd) = pdp_lim.get(n_fx, (min_pd, max_pd))
        min_pd = min(min_pd, old_min_pd)
        max_pd = max(max_pd, old_max_pd)
        pdp_lim[n_fx] = (min_pd, max_pd)
    if (2 in pdp_lim):
        Z_level = np.linspace(*pdp_lim[2], num=8)
    if (ax is None):
        fig = plt.figure(**fig_kw)
    else:
        fig = ax.get_figure()
        fig.clear()
    n_cols = min(n_cols, len(features))
    n_rows = int(np.ceil((len(features) / float(n_cols))))
    axs = []
    for (i, fx, name, (pdp, axes)) in zip(count(), features, names, pd_result):
        ax = fig.add_subplot(n_rows, n_cols, (i + 1))
        if (len(axes) == 1):
            ax.plot(axes[0], pdp[label_idx].ravel(), **line_kw)
        else:
            assert (len(axes) == 2)
            (XX, YY) = np.meshgrid(axes[0], axes[1])
            Z = pdp[label_idx].reshape(list(map(np.size, axes))).T
            CS = ax.contour(XX, YY, Z, levels=Z_level, linewidths=0.5, colors='k')
            ax.contourf(XX, YY, Z, levels=Z_level, vmax=Z_level[(- 1)], vmin=Z_level[0], alpha=0.75, **contour_kw)
            ax.clabel(CS, fmt='%2.2f', colors='k', fontsize=10, inline=True)
        deciles = mquantiles(X[:, fx[0]], prob=np.arange(0.1, 1.0, 0.1))
        trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
        ylim = ax.get_ylim()
        ax.vlines(deciles, [0], 0.05, transform=trans, color='k')
        ax.set_xlabel(name[0])
        ax.set_ylim(ylim)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6, prune='lower'))
        tick_formatter = ScalarFormatter()
        tick_formatter.set_powerlimits(((- 3), 4))
        ax.xaxis.set_major_formatter(tick_formatter)
        if (len(axes) > 1):
            deciles = mquantiles(X[:, fx[1]], prob=np.arange(0.1, 1.0, 0.1))
            trans = transforms.blended_transform_factory(ax.transAxes, ax.transData)
            xlim = ax.get_xlim()
            ax.hlines(deciles, [0], 0.05, transform=trans, color='k')
            ax.set_ylabel(name[1])
            ax.set_xlim(xlim)
        else:
            ax.set_ylabel('Partial dependence')
        if (len(axes) == 1):
            ax.set_ylim(pdp_lim[1])
        axs.append(ax)
    fig.subplots_adjust(bottom=0.15, top=0.7, left=0.1, right=0.95, wspace=0.4, hspace=0.3)
    return (fig, axs)
