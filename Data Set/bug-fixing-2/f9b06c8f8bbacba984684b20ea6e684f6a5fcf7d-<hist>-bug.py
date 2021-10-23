

@_preprocess_data(replace_names=['x', 'weights'], label_namer='x')
def hist(self, x, bins=None, range=None, normed=False, weights=None, cumulative=False, bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color=None, label=None, stacked=False, **kwargs):
    "\n        Plot a histogram.\n\n        Compute and draw the histogram of *x*. The return value is a\n        tuple (*n*, *bins*, *patches*) or ([*n0*, *n1*, ...], *bins*,\n        [*patches0*, *patches1*,...]) if the input contains multiple\n        data.\n\n        Multiple data can be provided via *x* as a list of datasets\n        of potentially different length ([*x0*, *x1*, ...]), or as\n        a 2-D ndarray in which each column is a dataset.  Note that\n        the ndarray form is transposed relative to the list form.\n\n        Masked arrays are not supported at present.\n\n        Parameters\n        ----------\n        x : (n,) array or sequence of (n,) arrays\n            Input values, this takes either a single array or a sequency of\n            arrays which are not required to be of the same length\n\n        bins : integer or array_like or 'auto', optional\n            If an integer is given, `bins + 1` bin edges are returned,\n            consistently with :func:`numpy.histogram` for numpy version >=\n            1.3.\n\n            Unequally spaced bins are supported if `bins` is a sequence.\n\n            If Numpy 1.11 is installed, may also be ``'auto'``.\n\n            Default is taken from the rcParam ``hist.bins``.\n\n        range : tuple or None, optional\n            The lower and upper range of the bins. Lower and upper outliers\n            are ignored. If not provided, `range` is (x.min(), x.max()). Range\n            has no effect if `bins` is a sequence.\n\n            If `bins` is a sequence or `range` is specified, autoscaling\n            is based on the specified bin range instead of the\n            range of x.\n\n            Default is ``None``\n\n        normed : boolean, optional\n            If `True`, the first element of the return tuple will\n            be the counts normalized to form a probability density, i.e.,\n            the area (or integral) under the histogram will sum to 1.\n            This is achieved dividing the count by the number of observations\n            times the bin width and *not* dividing by the total number\n            of observations. If `stacked` is also `True`, the sum of the\n            histograms is normalized to 1.\n\n            Default is ``False``\n\n        weights : (n, ) array_like or None, optional\n            An array of weights, of the same shape as `x`.  Each value in `x`\n            only contributes its associated weight towards the bin count\n            (instead of 1).  If `normed` is True, the weights are normalized,\n            so that the integral of the density over the range remains 1.\n\n            Default is ``None``\n\n        cumulative : boolean, optional\n            If `True`, then a histogram is computed where each bin gives the\n            counts in that bin plus all bins for smaller values. The last bin\n            gives the total number of datapoints.  If `normed` is also `True`\n            then the histogram is normalized such that the last bin equals 1.\n            If `cumulative` evaluates to less than 0 (e.g., -1), the direction\n            of accumulation is reversed.  In this case, if `normed` is also\n            `True`, then the histogram is normalized such that the first bin\n            equals 1.\n\n            Default is ``False``\n\n        bottom : array_like, scalar, or None\n            Location of the bottom baseline of each bin.  If a scalar,\n            the base line for each bin is shifted by the same amount.\n            If an array, each bin is shifted independently and the length\n            of bottom must match the number of bins.  If None, defaults to 0.\n\n            Default is ``None``\n\n        histtype : {'bar', 'barstacked', 'step',  'stepfilled'}, optional\n            The type of histogram to draw.\n\n            - 'bar' is a traditional bar-type histogram.  If multiple data\n              are given the bars are aranged side by side.\n\n            - 'barstacked' is a bar-type histogram where multiple\n              data are stacked on top of each other.\n\n            - 'step' generates a lineplot that is by default\n              unfilled.\n\n            - 'stepfilled' generates a lineplot that is by default\n              filled.\n\n            Default is 'bar'\n\n        align : {'left', 'mid', 'right'}, optional\n            Controls how the histogram is plotted.\n\n                - 'left': bars are centered on the left bin edges.\n\n                - 'mid': bars are centered between the bin edges.\n\n                - 'right': bars are centered on the right bin edges.\n\n            Default is 'mid'\n\n        orientation : {'horizontal', 'vertical'}, optional\n            If 'horizontal', `~matplotlib.pyplot.barh` will be used for\n            bar-type histograms and the *bottom* kwarg will be the left edges.\n\n        rwidth : scalar or None, optional\n            The relative width of the bars as a fraction of the bin width.  If\n            `None`, automatically compute the width.\n\n            Ignored if `histtype` is 'step' or 'stepfilled'.\n\n            Default is ``None``\n\n        log : boolean, optional\n            If `True`, the histogram axis will be set to a log scale. If `log`\n            is `True` and `x` is a 1D array, empty bins will be filtered out\n            and only the non-empty (`n`, `bins`, `patches`) will be returned.\n\n            Default is ``False``\n\n        color : color or array_like of colors or None, optional\n            Color spec or sequence of color specs, one per dataset.  Default\n            (`None`) uses the standard line color sequence.\n\n            Default is ``None``\n\n        label : string or None, optional\n            String, or sequence of strings to match multiple datasets.  Bar\n            charts yield multiple patches per dataset, but only the first gets\n            the label, so that the legend command will work as expected.\n\n            default is ``None``\n\n        stacked : boolean, optional\n            If `True`, multiple data are stacked on top of each other If\n            `False` multiple data are aranged side by side if histtype is\n            'bar' or on top of each other if histtype is 'step'\n\n            Default is ``False``\n\n        Returns\n        -------\n        n : array or list of arrays\n            The values of the histogram bins. See **normed** and **weights**\n            for a description of the possible semantics. If input **x** is an\n            array, then this is an array of length **nbins**. If input is a\n            sequence arrays ``[data1, data2,..]``, then this is a list of\n            arrays with the values of the histograms for each of the arrays\n            in the same order.\n\n        bins : array\n            The edges of the bins. Length nbins + 1 (nbins left edges and right\n            edge of last bin).  Always a single array even when multiple data\n            sets are passed in.\n\n        patches : list or list of lists\n            Silent list of individual patches used to create the histogram\n            or list of such list if multiple input datasets.\n\n        Other Parameters\n        ----------------\n        kwargs : `~matplotlib.patches.Patch` properties\n\n        See also\n        --------\n        hist2d : 2D histograms\n\n        Notes\n        -----\n        Until numpy release 1.5, the underlying numpy histogram function was\n        incorrect with `normed`=`True` if bin sizes were unequal.  MPL\n        inherited that error.  It is now corrected within MPL when using\n        earlier numpy versions.\n\n        Examples\n        --------\n        .. plot:: mpl_examples/statistics/histogram_demo_features.py\n\n        "

    def _normalize_input(inp, ename='input'):
        'Normalize 1 or 2d input into list of np.ndarray or\n            a single 2D np.ndarray.\n\n            Parameters\n            ----------\n            inp : iterable\n            ename : str, optional\n                Name to use in ValueError if `inp` can not be normalized\n\n            '
        if (isinstance(x, np.ndarray) or (not iterable(cbook.safe_first_element(inp)))):
            inp = np.asarray(inp)
            if (inp.ndim == 2):
                inp = inp.T
            elif (inp.ndim == 1):
                inp = inp.reshape(1, inp.shape[0])
            else:
                raise ValueError('{ename} must be 1D or 2D'.format(ename=ename))
            if (inp.shape[1] < inp.shape[0]):
                warnings.warn(('2D hist input should be nsamples x nvariables;\n this looks transposed (shape is %d x %d)' % inp.shape[::(- 1)]))
        else:
            inp = [np.asarray(xi) for xi in inp]
        return inp
    if (not self._hold):
        self.cla()
    if np.isscalar(x):
        x = [x]
    if (bins is None):
        bins = rcParams['hist.bins']
    bin_range = range
    range = __builtins__['range']
    if (histtype not in ['bar', 'barstacked', 'step', 'stepfilled']):
        raise ValueError(('histtype %s is not recognized' % histtype))
    if (align not in ['left', 'mid', 'right']):
        raise ValueError(('align kwarg %s is not recognized' % align))
    if (orientation not in ['horizontal', 'vertical']):
        raise ValueError(('orientation kwarg %s is not recognized' % orientation))
    if ((histtype == 'barstacked') and (not stacked)):
        stacked = True
    self._process_unit_info(xdata=x, kwargs=kwargs)
    x = self.convert_xunits(x)
    if (bin_range is not None):
        bin_range = self.convert_xunits(bin_range)
    binsgiven = (cbook.iterable(bins) or (bin_range is not None))
    flat = np.ravel(x)
    input_empty = (len(flat) == 0)
    if input_empty:
        x = np.array([[]])
    else:
        x = _normalize_input(x, 'x')
    nx = len(x)
    if (weights is not None):
        w = _normalize_input(weights, 'weights')
    else:
        w = ([None] * nx)
    if (len(w) != nx):
        raise ValueError('weights should have the same shape as x')
    for (xi, wi) in zip(x, w):
        if ((wi is not None) and (len(wi) != len(xi))):
            raise ValueError('weights should have the same shape as x')
    if (color is None):
        color = [self._get_lines.get_next_color() for i in xrange(nx)]
    else:
        color = mcolors.to_rgba_array(color)
        if (len(color) != nx):
            raise ValueError('color kwarg must have one color per dataset')
    _saved_bounds = self.dataLim.bounds
    if ((not binsgiven) and (not input_empty)):
        xmin = np.inf
        xmax = (- np.inf)
        for xi in x:
            if (len(xi) > 0):
                xmin = min(xmin, xi.min())
                xmax = max(xmax, xi.max())
        bin_range = (xmin, xmax)
    hist_kwargs = dict(range=bin_range)
    n = []
    mlast = None
    for i in xrange(nx):
        (m, bins) = np.histogram(x[i], bins, weights=w[i], **hist_kwargs)
        m = m.astype(float)
        if (mlast is None):
            mlast = np.zeros((len(bins) - 1), m.dtype)
        if (normed and (not stacked)):
            db = np.diff(bins)
            m = ((m.astype(float) / db) / m.sum())
        if stacked:
            if (mlast is None):
                mlast = np.zeros((len(bins) - 1), m.dtype)
            m += mlast
            mlast[:] = m
        n.append(m)
    if (stacked and normed):
        db = np.diff(bins)
        for m in n:
            m[:] = ((m.astype(float) / db) / n[(- 1)].sum())
    if cumulative:
        slc = slice(None)
        if (cbook.is_numlike(cumulative) and (cumulative < 0)):
            slc = slice(None, None, (- 1))
        if normed:
            n = [(m * np.diff(bins))[slc].cumsum()[slc] for m in n]
        else:
            n = [m[slc].cumsum()[slc] for m in n]
    if (orientation == 'horizontal'):
        margins = {
            'left': False,
        }
    else:
        margins = {
            'bottom': False,
        }
    patches = []
    if histtype.startswith('bar'):
        _saved_autoscalex = self.get_autoscalex_on()
        _saved_autoscaley = self.get_autoscaley_on()
        self.set_autoscalex_on(False)
        self.set_autoscaley_on(False)
        totwidth = np.diff(bins)
        if (rwidth is not None):
            dr = min(1.0, max(0.0, rwidth))
        elif ((len(n) > 1) and ((not stacked) or rcParams['_internal.classic_mode'])):
            dr = 0.8
        else:
            dr = 1.0
        if ((histtype == 'bar') and (not stacked)):
            width = ((dr * totwidth) / nx)
            dw = width
            if (nx > 1):
                boffset = ((((- 0.5) * dr) * totwidth) * (1.0 - (1.0 / nx)))
            else:
                boffset = 0.0
            stacked = False
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
        for (m, c) in zip(n, color):
            if (bottom is None):
                bottom = np.zeros(len(m), float)
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
        self.set_autoscalex_on(_saved_autoscalex)
        self.set_autoscaley_on(_saved_autoscaley)
        self.autoscale_view()
    elif histtype.startswith('step'):
        x = np.zeros(((4 * len(bins)) - 3), float)
        y = np.zeros(((4 * len(bins)) - 3), float)
        (x[0:((2 * len(bins)) - 1):2], x[1:((2 * len(bins)) - 1):2]) = (bins, bins[:(- 1)])
        x[((2 * len(bins)) - 1):] = x[1:((2 * len(bins)) - 1)][::(- 1)]
        if (bottom is None):
            bottom = np.zeros((len(bins) - 1), float)
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
            elif (normed or (weights is not None)):
                ndata = np.array(n)
                minimum = (np.min(ndata[(ndata > 0)]) / logbase)
            else:
                minimum = (1.0 / logbase)
            (y[0], y[(- 1)]) = (minimum, minimum)
        else:
            minimum = np.min(bins)
        if ((align == 'left') or (align == 'center')):
            x -= (0.5 * (bins[1] - bins[0]))
        elif (align == 'right'):
            x += (0.5 * (bins[1] - bins[0]))
        fill = (histtype == 'stepfilled')
        (xvals, yvals) = ([], [])
        for m in n:
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
            patches.append(self.fill(x[:split], y[:split], closed=(True if fill else None), facecolor=c, edgecolor=(None if fill else c), fill=(fill if fill else None), margins=margins))
        patches.reverse()
        if (orientation == 'horizontal'):
            xmin0 = max((_saved_bounds[0] * 0.9), minimum)
            xmax = self.dataLim.intervalx[1]
            for m in n:
                if (np.sum(m) > 0):
                    xmin = np.amin(m[(m != 0)])
            xmin = (max((xmin * 0.9), minimum) if (not input_empty) else minimum)
            xmin = min(xmin0, xmin)
            self.dataLim.intervalx = (xmin, xmax)
        elif (orientation == 'vertical'):
            ymin0 = max((_saved_bounds[1] * 0.9), minimum)
            ymax = self.dataLim.intervaly[1]
            for m in n:
                if (np.sum(m) > 0):
                    ymin = np.amin(m[(m != 0)])
            ymin = (max((ymin * 0.9), minimum) if (not input_empty) else minimum)
            ymin = min(ymin0, ymin)
            self.dataLim.intervaly = (ymin, ymax)
    if (label is None):
        labels = [None]
    elif is_string_like(label):
        labels = [label]
    else:
        labels = [six.text_type(lab) for lab in label]
    for (patch, lbl) in zip_longest(patches, labels, fillvalue=None):
        if patch:
            p = patch[0]
            p.update(kwargs)
            if (lbl is not None):
                p.set_label(lbl)
            for p in patch[1:]:
                p.update(kwargs)
                p.set_label('_nolegend_')
    if binsgiven:
        if (orientation == 'vertical'):
            self.update_datalim([(bins[0], 0), (bins[(- 1)], 0)], updatey=False)
        else:
            self.update_datalim([(0, bins[0]), (0, bins[(- 1)])], updatex=False)
    if (nx == 1):
        return (n[0], bins, cbook.silent_list('Patch', patches[0]))
    else:
        return (n, bins, cbook.silent_list('Lists of Patches', patches))
