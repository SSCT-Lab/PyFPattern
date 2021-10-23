def bxp(self, bxpstats, positions=None, widths=None, vert=True, patch_artist=False, shownotches=False, showmeans=False, showcaps=True, showbox=True, showfliers=True, boxprops=None, whiskerprops=None, flierprops=None, medianprops=None, capprops=None, meanprops=None, meanline=False, manage_xticks=True):
    "\n        Drawing function for box and whisker plots.\n\n        Call signature::\n\n          bxp(self, bxpstats, positions=None, widths=None, vert=True,\n              patch_artist=False, shownotches=False, showmeans=False,\n              showcaps=True, showbox=True, showfliers=True,\n              boxprops=None, whiskerprops=None, flierprops=None,\n              medianprops=None, capprops=None, meanprops=None,\n              meanline=False, manage_xticks=True):\n\n        Make a box and whisker plot for each column of *x* or each\n        vector in sequence *x*.  The box extends from the lower to\n        upper quartile values of the data, with a line at the median.\n        The whiskers extend from the box to show the range of the\n        data.  Flier points are those past the end of the whiskers.\n\n        Parameters\n        ----------\n\n        bxpstats : list of dicts\n          A list of dictionaries containing stats for each boxplot.\n          Required keys are:\n\n          - ``med``: The median (scalar float).\n\n          - ``q1``: The first quartile (25th percentile) (scalar\n            float).\n\n          - ``q3``: The third quartile (75th percentile) (scalar\n            float).\n\n          - ``whislo``: Lower bound of the lower whisker (scalar\n            float).\n\n          - ``whishi``: Upper bound of the upper whisker (scalar\n            float).\n\n          Optional keys are:\n\n          - ``mean``: The mean (scalar float). Needed if\n            ``showmeans=True``.\n\n          - ``fliers``: Data beyond the whiskers (sequence of floats).\n            Needed if ``showfliers=True``.\n\n          - ``cilo`` & ``cihi``: Lower and upper confidence intervals\n            about the median. Needed if ``shownotches=True``.\n\n          - ``label``: Name of the dataset (string). If available,\n            this will be used a tick label for the boxplot\n\n        positions : array-like, default = [1, 2, ..., n]\n          Sets the positions of the boxes. The ticks and limits\n          are automatically set to match the positions.\n\n        widths : array-like, default = 0.5\n          Either a scalar or a vector and sets the width of each\n          box. The default is 0.5, or ``0.15*(distance between extreme\n          positions)`` if that is smaller.\n\n        vert : bool, default = False\n          If `True` (default), makes the boxes vertical.  If `False`,\n          makes horizontal boxes.\n\n        patch_artist : bool, default = False\n          If `False` produces boxes with the\n          `~matplotlib.lines.Line2D` artist.  If `True` produces boxes\n          with the `~matplotlib.patches.Patch` artist.\n\n        shownotches : bool, default = False\n          If `False` (default), produces a rectangular box plot.\n          If `True`, will produce a notched box plot\n\n        showmeans : bool, default = False\n          If `True`, will toggle on the rendering of the means\n\n        showcaps  : bool, default = True\n          If `True`, will toggle on the rendering of the caps\n\n        showbox  : bool, default = True\n          If `True`, will toggle on the rendering of the box\n\n        showfliers : bool, default = True\n          If `True`, will toggle on the rendering of the fliers\n\n        boxprops : dict or None (default)\n          If provided, will set the plotting style of the boxes\n\n        whiskerprops : dict or None (default)\n          If provided, will set the plotting style of the whiskers\n\n        capprops : dict or None (default)\n          If provided, will set the plotting style of the caps\n\n        flierprops : dict or None (default)\n          If provided will set the plotting style of the fliers\n\n        medianprops : dict or None (default)\n          If provided, will set the plotting style of the medians\n\n        meanprops : dict or None (default)\n          If provided, will set the plotting style of the means\n\n        meanline : bool, default = False\n          If `True` (and *showmeans* is `True`), will try to render the mean\n          as a line spanning the full width of the box according to\n          *meanprops*. Not recommended if *shownotches* is also True.\n          Otherwise, means will be shown as points.\n\n        manage_xticks : bool, default = True\n          If the function should adjust the xlim and xtick locations.\n\n        Returns\n        -------\n        result : dict\n          A dictionary mapping each component of the boxplot to a list\n          of the :class:`matplotlib.lines.Line2D` instances\n          created. That dictionary has the following keys (assuming\n          vertical boxplots):\n\n          - ``boxes``: the main body of the boxplot showing the\n            quartiles and the median's confidence intervals if\n            enabled.\n\n          - ``medians``: horizontal lines at the median of each box.\n\n          - ``whiskers``: the vertical lines extending to the most\n            extreme, non-outlier data points.\n\n          - ``caps``: the horizontal lines at the ends of the\n            whiskers.\n\n          - ``fliers``: points representing data that extend beyond\n            the whiskers (fliers).\n\n          - ``means``: points or lines representing the means.\n\n        Examples\n        --------\n\n        .. plot:: mpl_examples/statistics/bxp_demo.py\n\n        "
    whiskers = []
    caps = []
    boxes = []
    medians = []
    means = []
    fliers = []
    datalabels = []
    linestyle_map = {
        'solid': '-',
        'dashed': '--',
        'dashdot': '-.',
        'dotted': ':',
    }
    zorder = mlines.Line2D.zorder
    zdelta = 0.1
    if patch_artist:
        final_boxprops = dict(linestyle=rcParams['boxplot.boxprops.linestyle'], edgecolor=rcParams['boxplot.boxprops.color'], facecolor=rcParams['patch.facecolor'], linewidth=rcParams['boxplot.boxprops.linewidth'])
        if rcParams['_internal.classic_mode']:
            final_boxprops['facecolor'] = 'white'
    else:
        final_boxprops = dict(linestyle=rcParams['boxplot.boxprops.linestyle'], color=rcParams['boxplot.boxprops.color'])
    final_boxprops['zorder'] = zorder
    if (boxprops is not None):
        final_boxprops.update(boxprops)
    final_whiskerprops = dict(linestyle=rcParams['boxplot.whiskerprops.linestyle'], linewidth=rcParams['boxplot.whiskerprops.linewidth'], color=rcParams['boxplot.whiskerprops.color'])
    final_capprops = dict(linestyle=rcParams['boxplot.capprops.linestyle'], linewidth=rcParams['boxplot.capprops.linewidth'], color=rcParams['boxplot.capprops.color'])
    final_capprops['zorder'] = zorder
    if (capprops is not None):
        final_capprops.update(capprops)
    final_whiskerprops['zorder'] = zorder
    if (whiskerprops is not None):
        final_whiskerprops.update(whiskerprops)
    final_flierprops = dict(linestyle=rcParams['boxplot.flierprops.linestyle'], linewidth=rcParams['boxplot.flierprops.linewidth'], color=rcParams['boxplot.flierprops.color'], marker=rcParams['boxplot.flierprops.marker'], markerfacecolor=rcParams['boxplot.flierprops.markerfacecolor'], markeredgecolor=rcParams['boxplot.flierprops.markeredgecolor'], markersize=rcParams['boxplot.flierprops.markersize'])
    final_flierprops['zorder'] = zorder
    if (flierprops is not None):
        final_flierprops.update(flierprops)
    final_medianprops = dict(linestyle=rcParams['boxplot.medianprops.linestyle'], linewidth=rcParams['boxplot.medianprops.linewidth'], color=rcParams['boxplot.medianprops.color'])
    final_medianprops['zorder'] = (zorder + zdelta)
    if (medianprops is not None):
        final_medianprops.update(medianprops)
    if meanline:
        final_meanprops = dict(linestyle=rcParams['boxplot.meanprops.linestyle'], linewidth=rcParams['boxplot.meanprops.linewidth'], color=rcParams['boxplot.meanprops.color'])
    else:
        final_meanprops = dict(linestyle='', marker=rcParams['boxplot.meanprops.marker'], markerfacecolor=rcParams['boxplot.meanprops.markerfacecolor'], markeredgecolor=rcParams['boxplot.meanprops.markeredgecolor'], markersize=rcParams['boxplot.meanprops.markersize'])
    final_meanprops['zorder'] = (zorder + zdelta)
    if (meanprops is not None):
        final_meanprops.update(meanprops)

    def to_vc(xs, ys):
        verts = []
        for (xi, yi) in zip(xs, ys):
            verts.append((xi, yi))
        verts.append((0, 0))
        codes = (([mpath.Path.MOVETO] + ([mpath.Path.LINETO] * (len(verts) - 2))) + [mpath.Path.CLOSEPOLY])
        return (verts, codes)

    def patch_list(xs, ys, **kwargs):
        (verts, codes) = to_vc(xs, ys)
        path = mpath.Path(verts, codes)
        patch = mpatches.PathPatch(path, **kwargs)
        self.add_artist(patch)
        return [patch]
    if vert:

        def doplot(*args, **kwargs):
            return self.plot(*args, **kwargs)

        def dopatch(xs, ys, **kwargs):
            return patch_list(xs, ys, **kwargs)
    else:

        def doplot(*args, **kwargs):
            shuffled = []
            for i in xrange(0, len(args), 2):
                shuffled.extend([args[(i + 1)], args[i]])
            return self.plot(*shuffled, **kwargs)

        def dopatch(xs, ys, **kwargs):
            (xs, ys) = (ys, xs)
            return patch_list(xs, ys, **kwargs)
    N = len(bxpstats)
    datashape_message = 'List of boxplot statistics and `{0}` values must have same the length'
    if (positions is None):
        positions = list(xrange(1, (N + 1)))
    elif (len(positions) != N):
        raise ValueError(datashape_message.format('positions'))
    if (widths is None):
        distance = (max(positions) - min(positions))
        widths = ([min((0.15 * max(distance, 1.0)), 0.5)] * N)
    elif np.isscalar(widths):
        widths = ([widths] * N)
    elif (len(widths) != N):
        raise ValueError(datashape_message.format('widths'))
    if (not self._hold):
        self.cla()
    holdStatus = self._hold
    for (pos, width, stats) in zip(positions, widths, bxpstats):
        datalabels.append(stats.get('label', pos))
        flier_x = (np.ones(len(stats['fliers'])) * pos)
        flier_y = stats['fliers']
        whisker_x = (np.ones(2) * pos)
        whiskerlo_y = np.array([stats['q1'], stats['whislo']])
        whiskerhi_y = np.array([stats['q3'], stats['whishi']])
        cap_left = (pos - (width * 0.25))
        cap_right = (pos + (width * 0.25))
        cap_x = np.array([cap_left, cap_right])
        cap_lo = (np.ones(2) * stats['whislo'])
        cap_hi = (np.ones(2) * stats['whishi'])
        box_left = (pos - (width * 0.5))
        box_right = (pos + (width * 0.5))
        med_y = [stats['med'], stats['med']]
        if shownotches:
            box_x = [box_left, box_right, box_right, cap_right, box_right, box_right, box_left, box_left, cap_left, box_left, box_left]
            box_y = [stats['q1'], stats['q1'], stats['cilo'], stats['med'], stats['cihi'], stats['q3'], stats['q3'], stats['cihi'], stats['med'], stats['cilo'], stats['q1']]
            med_x = cap_x
        else:
            box_x = [box_left, box_right, box_right, box_left, box_left]
            box_y = [stats['q1'], stats['q1'], stats['q3'], stats['q3'], stats['q1']]
            med_x = [box_left, box_right]
        if showbox:
            if patch_artist:
                boxes.extend(dopatch(box_x, box_y, **final_boxprops))
            else:
                boxes.extend(doplot(box_x, box_y, **final_boxprops))
        whiskers.extend(doplot(whisker_x, whiskerlo_y, **final_whiskerprops))
        whiskers.extend(doplot(whisker_x, whiskerhi_y, **final_whiskerprops))
        if showcaps:
            caps.extend(doplot(cap_x, cap_lo, **final_capprops))
            caps.extend(doplot(cap_x, cap_hi, **final_capprops))
        medians.extend(doplot(med_x, med_y, **final_medianprops))
        if showmeans:
            if meanline:
                means.extend(doplot([box_left, box_right], [stats['mean'], stats['mean']], **final_meanprops))
            else:
                means.extend(doplot([pos], [stats['mean']], **final_meanprops))
        if showfliers:
            fliers.extend(doplot(flier_x, flier_y, **final_flierprops))
    if vert:
        setticks = self.set_xticks
        setlim = self.set_xlim
        setlabels = self.set_xticklabels
    else:
        setticks = self.set_yticks
        setlim = self.set_ylim
        setlabels = self.set_yticklabels
    if manage_xticks:
        newlimits = ((min(positions) - 0.5), (max(positions) + 0.5))
        setlim(newlimits)
        setticks(positions)
        setlabels(datalabels)
    self.hold(holdStatus)
    return dict(whiskers=whiskers, caps=caps, boxes=boxes, medians=medians, fliers=fliers, means=means)