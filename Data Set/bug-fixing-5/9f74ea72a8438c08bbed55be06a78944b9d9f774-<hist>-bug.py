@_preprocess_data(replace_names=['x', 'weights'], label_namer='x')
def hist(self, x, bins=None, range=None, density=None, weights=None, cumulative=False, bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color=None, label=None, stacked=False, normed=None, **kwargs):
    "\n        Plot a histogram.\n\n        Compute and draw the histogram of *x*. The return value is a\n        tuple (*n*, *bins*, *patches*) or ([*n0*, *n1*, ...], *bins*,\n        [*patches0*, *patches1*,...]) if the input contains multiple\n        data.\n\n        Multiple data can be provided via *x* as a list of datasets\n        of potentially different length ([*x0*, *x1*, ...]), or as\n        a 2-D ndarray in which each column is a dataset.  Note that\n        the ndarray form is transposed relative to the list form.\n\n        Masked arrays are not supported at present.\n\n        Parameters\n        ----------\n        x : (n,) array or sequence of (n,) arrays\n            Input values, this takes either a single array or a sequence of\n            arrays which are not required to be of the same length.\n\n        bins : int or sequence or str, optional\n            If an integer is given, ``bins + 1`` bin edges are calculated and\n            returned, consistent with `numpy.histogram`.\n\n            If `bins` is a sequence, gives bin edges, including left edge of\n            first bin and right edge of last bin.  In this case, `bins` is\n            returned unmodified.\n\n            All but the last (righthand-most) bin is half-open.  In other\n            words, if `bins` is::\n\n                [1, 2, 3, 4]\n\n            then the first bin is ``[1, 2)`` (including 1, but excluding 2) and\n            the second ``[2, 3)``.  The last bin, however, is ``[3, 4]``, which\n            *includes* 4.\n\n            Unequally spaced bins are supported if *bins* is a sequence.\n\n            With Numpy 1.11 or newer, you can alternatively provide a string\n            describing a binning strategy, such as 'auto', 'sturges', 'fd',\n            'doane', 'scott', 'rice', 'sturges' or 'sqrt', see\n            `numpy.histogram`.\n\n            The default is taken from :rc:`hist.bins`.\n\n        range : tuple or None, optional\n            The lower and upper range of the bins. Lower and upper outliers\n            are ignored. If not provided, *range* is ``(x.min(), x.max())``.\n            Range has no effect if *bins* is a sequence.\n\n            If *bins* is a sequence or *range* is specified, autoscaling\n            is based on the specified bin range instead of the\n            range of x.\n\n            Default is ``None``\n\n        density : bool, optional\n            If ``True``, the first element of the return tuple will\n            be the counts normalized to form a probability density, i.e.,\n            the area (or integral) under the histogram will sum to 1.\n            This is achieved by dividing the count by the number of\n            observations times the bin width and not dividing by the total\n            number of observations. If *stacked* is also ``True``, the sum of\n            the histograms is normalized to 1.\n\n            Default is ``None`` for both *normed* and *density*. If either is\n            set, then that value will be used. If neither are set, then the\n            args will be treated as ``False``.\n\n            If both *density* and *normed* are set an error is raised.\n\n        weights : (n, ) array_like or None, optional\n            An array of weights, of the same shape as *x*.  Each value in *x*\n            only contributes its associated weight towards the bin count\n            (instead of 1).  If *normed* or *density* is ``True``,\n            the weights are normalized, so that the integral of the density\n            over the range remains 1.\n\n            Default is ``None``\n\n        cumulative : bool, optional\n            If ``True``, then a histogram is computed where each bin gives the\n            counts in that bin plus all bins for smaller values. The last bin\n            gives the total number of datapoints. If *normed* or *density*\n            is also ``True`` then the histogram is normalized such that the\n            last bin equals 1. If *cumulative* evaluates to less than 0\n            (e.g., -1), the direction of accumulation is reversed.\n            In this case, if *normed* and/or *density* is also ``True``, then\n            the histogram is normalized such that the first bin equals 1.\n\n            Default is ``False``\n\n        bottom : array_like, scalar, or None\n            Location of the bottom baseline of each bin.  If a scalar,\n            the base line for each bin is shifted by the same amount.\n            If an array, each bin is shifted independently and the length\n            of bottom must match the number of bins.  If None, defaults to 0.\n\n            Default is ``None``\n\n        histtype : {'bar', 'barstacked', 'step',  'stepfilled'}, optional\n            The type of histogram to draw.\n\n            - 'bar' is a traditional bar-type histogram.  If multiple data\n              are given the bars are arranged side by side.\n\n            - 'barstacked' is a bar-type histogram where multiple\n              data are stacked on top of each other.\n\n            - 'step' generates a lineplot that is by default\n              unfilled.\n\n            - 'stepfilled' generates a lineplot that is by default\n              filled.\n\n            Default is 'bar'\n\n        align : {'left', 'mid', 'right'}, optional\n            Controls how the histogram is plotted.\n\n                - 'left': bars are centered on the left bin edges.\n\n                - 'mid': bars are centered between the bin edges.\n\n                - 'right': bars are centered on the right bin edges.\n\n            Default is 'mid'\n\n        orientation : {'horizontal', 'vertical'}, optional\n            If 'horizontal', `~matplotlib.pyplot.barh` will be used for\n            bar-type histograms and the *bottom* kwarg will be the left edges.\n\n        rwidth : scalar or None, optional\n            The relative width of the bars as a fraction of the bin width.  If\n            ``None``, automatically compute the width.\n\n            Ignored if *histtype* is 'step' or 'stepfilled'.\n\n            Default is ``None``\n\n        log : bool, optional\n            If ``True``, the histogram axis will be set to a log scale. If\n            *log* is ``True`` and *x* is a 1D array, empty bins will be\n            filtered out and only the non-empty ``(n, bins, patches)``\n            will be returned.\n\n            Default is ``False``\n\n        color : color or array_like of colors or None, optional\n            Color spec or sequence of color specs, one per dataset.  Default\n            (``None``) uses the standard line color sequence.\n\n            Default is ``None``\n\n        label : str or None, optional\n            String, or sequence of strings to match multiple datasets.  Bar\n            charts yield multiple patches per dataset, but only the first gets\n            the label, so that the legend command will work as expected.\n\n            default is ``None``\n\n        stacked : bool, optional\n            If ``True``, multiple data are stacked on top of each other If\n            ``False`` multiple data are arranged side by side if histtype is\n            'bar' or on top of each other if histtype is 'step'\n\n            Default is ``False``\n\n        normed : bool, optional\n            Deprecated; use the density keyword argument instead.\n\n        Returns\n        -------\n        n : array or list of arrays\n            The values of the histogram bins. See *normed* or *density*\n            and *weights* for a description of the possible semantics.\n            If input *x* is an array, then this is an array of length\n            *nbins*. If input is a sequence arrays\n            ``[data1, data2,..]``, then this is a list of arrays with\n            the values of the histograms for each of the arrays in the\n            same order.\n\n        bins : array\n            The edges of the bins. Length nbins + 1 (nbins left edges and right\n            edge of last bin).  Always a single array even when multiple data\n            sets are passed in.\n\n        patches : list or list of lists\n            Silent list of individual patches used to create the histogram\n            or list of such list if multiple input datasets.\n\n        Other Parameters\n        ----------------\n        **kwargs : `~matplotlib.patches.Patch` properties\n\n        See also\n        --------\n        hist2d : 2D histograms\n\n        Notes\n        -----\n        .. [Notes section required for data comment. See #10189.]\n\n        "
    bin_range = range
    from builtins import range
    if np.isscalar(x):
        x = [x]
    if (bins is None):
        bins = rcParams['hist.bins']
    if (histtype not in ['bar', 'barstacked', 'step', 'stepfilled']):
        raise ValueError(('histtype %s is not recognized' % histtype))
    if (align not in ['left', 'mid', 'right']):
        raise ValueError(('align kwarg %s is not recognized' % align))
    if (orientation not in ['horizontal', 'vertical']):
        raise ValueError(('orientation kwarg %s is not recognized' % orientation))
    if ((histtype == 'barstacked') and (not stacked)):
        stacked = True
    if ((density is not None) and (normed is not None)):
        raise ValueError("kwargs 'density' and 'normed' cannot be used simultaneously. Please only use 'density', since 'normed'is deprecated.")
    if (normed is not None):
        cbook.warn_deprecated('2.1', name="'normed'", obj_type='kwarg', alternative="'density'", removal='3.1')
    input_empty = (np.size(x) == 0)
    if input_empty:
        x = [np.array([])]
    else:
        x = cbook._reshape_2D(x, 'x')
    nx = len(x)
    self._process_unit_info(xdata=x[0], kwargs=kwargs)
    x = [self.convert_xunits(xi) for xi in x]
    if (bin_range is not None):
        bin_range = self.convert_xunits(bin_range)
    binsgiven = (cbook.iterable(bins) or (bin_range is not None))
    if (weights is not None):
        w = cbook._reshape_2D(weights, 'weights')
    else:
        w = ([None] * nx)
    if (len(w) != nx):
        raise ValueError('weights should have the same shape as x')
    for (xi, wi) in zip(x, w):
        if ((wi is not None) and (len(wi) != len(xi))):
            raise ValueError('weights should have the same shape as x')
    if (color is None):
        color = [self._get_lines.get_next_color() for i in range(nx)]
    else:
        color = mcolors.to_rgba_array(color)
        if (len(color) != nx):
            raise ValueError('color kwarg must have one color per dataset')
    if ((not binsgiven) and (not input_empty)):
        xmin = np.inf
        xmax = (- np.inf)
        for xi in x:
            if (len(xi) > 0):
                xmin = min(xmin, np.nanmin(xi))
                xmax = max(xmax, np.nanmax(xi))
        bin_range = (xmin, xmax)
    density = (bool(density) or bool(normed))
    if (density and (not stacked)):
        hist_kwargs = dict(range=bin_range, density=density)
    else:
        hist_kwargs = dict(range=bin_range)
    tops = []
    mlast = None
    for i in range(nx):
        (m, bins) = np.histogram(x[i], bins, weights=w[i], **hist_kwargs)
        m = m.astype(float)
        if (mlast is None):
            mlast = np.zeros((len(bins) - 1), m.dtype)
        if stacked:
            m += mlast
            mlast[:] = m
        tops.append(m)
    if (stacked and density):
        db = np.diff(bins)
        for m in tops:
            m[:] = ((m / db) / tops[(- 1)].sum())
    if cumulative:
        slc = slice(None)
        if (isinstance(cumulative, Number) and (cumulative < 0)):
            slc = slice(None, None, (- 1))
        if density:
            tops = [(m * np.diff(bins))[slc].cumsum()[slc] for m in tops]
        else:
            tops = [m[slc].cumsum()[slc] for m in tops]
    patches = []
    _saved_autoscalex = self.get_autoscalex_on()
    _saved_autoscaley = self.get_autoscaley_on()
    self.set_autoscalex_on(False)
    self.set_autoscaley_on(False)
    if histtype.startswith('bar'):
        totwidth = np.diff(bins)
        if (rwidth is not None):
            dr = np.clip(rwidth, 0, 1)
        elif ((len(tops) > 1) and ((not stacked) or rcParams['_internal.classic_mode'])):
            dr = 0.8
        else:
            dr = 1.0
        if ((histtype == 'bar') and (not stacked)):
            width = ((dr * totwidth) / nx)
            dw = width
            boffset = ((((- 0.5) * dr) * totwidth) * (1 - (1 / nx)))
        elif ((histtype == 'barstacked') or stacked):
            width = (dr * totwidth)
            (boffset, dw) = (0.0, 0.0)
        if ((align == 'mid') or (align == 'edge')):
            boffset += (0.5 * totwidth)
        elif (align == 'right'):
            boffset += totwidth
        if (orientation == 'horizontal'):
            _barfunc = self.barh
            bottom_kwarg = 'left'
        else:
            _barfunc = self.bar
            bottom_kwarg = 'bottom'
        for (m, c) in zip(tops, color):
            if (bottom is None):
                bottom = np.zeros(len(m))
            if stacked:
                height = (m - bottom)
            else:
                height = m
            patch = _barfunc((bins[:(- 1)] + boffset), height, width, align='center', log=log, color=c, **{
                bottom_kwarg: bottom,
            })
            patches.append(patch)
            if stacked:
                bottom[:] = m
            boffset += dw
    elif histtype.startswith('step'):
        x = np.zeros(((4 * len(bins)) - 3))
        y = np.zeros(((4 * len(bins)) - 3))
        (x[0:((2 * len(bins)) - 1):2], x[1:((2 * len(bins)) - 1):2]) = (bins, bins[:(- 1)])
        x[((2 * len(bins)) - 1):] = x[1:((2 * len(bins)) - 1)][::(- 1)]
        if (bottom is None):
            bottom = np.zeros((len(bins) - 1))
        (y[1:((2 * len(bins)) - 1):2], y[2:(2 * len(bins)):2]) = (bottom, bottom)
        y[((2 * len(bins)) - 1):] = y[1:((2 * len(bins)) - 1)][::(- 1)]
        if log:
            if (orientation == 'horizontal'):
                self.set_xscale('log', nonposx='clip')
                logbase = self.xaxis._scale.base
            else:
                self.set_yscale('log', nonposy='clip')
                logbase = self.yaxis._scale.base
            if (np.min(bottom) > 0):
                minimum = np.min(bottom)
            elif (density or (weights is not None)):
                ndata = np.array(tops)
                minimum = (np.min(ndata[(ndata > 0)]) / logbase)
            else:
                minimum = (1.0 / logbase)
            (y[0], y[(- 1)]) = (minimum, minimum)
        else:
            minimum = 0
        if ((align == 'left') or (align == 'center')):
            x -= (0.5 * (bins[1] - bins[0]))
        elif (align == 'right'):
            x += (0.5 * (bins[1] - bins[0]))
        fill = (histtype == 'stepfilled')
        (xvals, yvals) = ([], [])
        for m in tops:
            if stacked:
                y[0] = y[1]
                y[((2 * len(bins)) - 1):] = y[1:((2 * len(bins)) - 1)][::(- 1)]
            (y[1:((2 * len(bins)) - 1):2], y[2:(2 * len(bins)):2]) = ((m + bottom), (m + bottom))
            if log:
                y[(y < minimum)] = minimum
            if (orientation == 'horizontal'):
                xvals.append(y.copy())
                yvals.append(x.copy())
            else:
                xvals.append(x.copy())
                yvals.append(y.copy())
        split = ((- 1) if fill else (2 * len(bins)))
        for (x, y, c) in reversed(list(zip(xvals, yvals, color))):
            patches.append(self.fill(x[:split], y[:split], closed=(True if fill else None), facecolor=c, edgecolor=(None if fill else c), fill=(fill if fill else None)))
        for patch_list in patches:
            for patch in patch_list:
                if (orientation == 'vertical'):
                    patch.sticky_edges.y.append(minimum)
                elif (orientation == 'horizontal'):
                    patch.sticky_edges.x.append(minimum)
        patches.reverse()
    self.set_autoscalex_on(_saved_autoscalex)
    self.set_autoscaley_on(_saved_autoscaley)
    self.autoscale_view()
    if (label is None):
        labels = [None]
    elif isinstance(label, str):
        labels = [label]
    else:
        labels = [str(lab) for lab in label]
    for (patch, lbl) in itertools.zip_longest(patches, labels):
        if patch:
            p = patch[0]
            p.update(kwargs)
            if (lbl is not None):
                p.set_label(lbl)
            for p in patch[1:]:
                p.update(kwargs)
                p.set_label('_nolegend_')
    if (nx == 1):
        return (tops[0], bins, cbook.silent_list('Patch', patches[0]))
    else:
        return (tops, bins, cbook.silent_list('Lists of Patches', patches))