@_preprocess_data(replace_names=['x', 'y', 'xerr', 'yerr'], label_namer='y')
@docstring.dedent_interpd
def errorbar(self, x, y, yerr=None, xerr=None, fmt='', ecolor=None, elinewidth=None, capsize=None, barsabove=False, lolims=False, uplims=False, xlolims=False, xuplims=False, errorevery=1, capthick=None, **kwargs):
    "\n        Plot an errorbar graph.\n\n        Plot x versus y with error deltas in yerr and xerr.\n        Vertical errorbars are plotted if yerr is not None.\n        Horizontal errorbars are plotted if xerr is not None.\n\n        x, y, xerr, and yerr can all be scalars, which plots a\n        single error bar at x, y.\n\n        Parameters\n        ----------\n        x : scalar or array-like\n        y : scalar or array-like\n\n        xerr/yerr : scalar or array-like, shape(N,) or shape(2,N), optional\n            If a scalar number, len(N) array-like object, or a N-element\n            array-like object, errorbars are drawn at +/-value relative\n            to the data. Default is None.\n\n            If a sequence of shape 2xN, errorbars are drawn at -row1\n            and +row2 relative to the data.\n\n        fmt : plot format string, optional, default: None\n            The plot format symbol. If fmt is 'none' (case-insensitive),\n            only the errorbars are plotted.  This is used for adding\n            errorbars to a bar plot, for example.  Default is '',\n            an empty plot format string; properties are\n            then identical to the defaults for :meth:`plot`.\n\n        ecolor : mpl color, optional, default: None\n            A matplotlib color arg which gives the color the errorbar lines;\n            if None, use the color of the line connecting the markers.\n\n        elinewidth : scalar, optional, default: None\n            The linewidth of the errorbar lines. If None, use the linewidth.\n\n        capsize : scalar, optional, default: None\n            The length of the error bar caps in points; if None, it will\n            take the value from ``errorbar.capsize``\n            :data:`rcParam<matplotlib.rcParams>`.\n\n        capthick : scalar, optional, default: None\n            An alias kwarg to markeredgewidth (a.k.a. - mew). This\n            setting is a more sensible name for the property that\n            controls the thickness of the error bar cap in points. For\n            backwards compatibility, if mew or markeredgewidth are given,\n            then they will over-ride capthick. This may change in future\n            releases.\n\n        barsabove : bool, optional, default: False\n            if True , will plot the errorbars above the plot\n            symbols. Default is below.\n\n        lolims / uplims / xlolims / xuplims : bool, optional, default:None\n            These arguments can be used to indicate that a value gives\n            only upper/lower limits. In that case a caret symbol is\n            used to indicate this. lims-arguments may be of the same\n            type as *xerr* and *yerr*.  To use limits with inverted\n            axes, :meth:`set_xlim` or :meth:`set_ylim` must be called\n            before :meth:`errorbar`.\n\n        errorevery : positive integer, optional, default:1\n            subsamples the errorbars. e.g., if errorevery=5, errorbars for\n            every 5-th datapoint will be plotted. The data plot itself still\n            shows all data points.\n\n        Returns\n        -------\n        plotline : :class:`~matplotlib.lines.Line2D` instance\n            x, y plot markers and/or line\n        caplines : list of :class:`~matplotlib.lines.Line2D` instances\n            error bar cap\n        barlinecols : list of :class:`~matplotlib.collections.LineCollection`\n            horizontal and vertical error ranges.\n\n        Other Parameters\n        ----------------\n        **kwargs :\n            All other keyword arguments are passed on to the plot\n            command for the markers. For example, this code makes big red\n            squares with thick green edges::\n\n                x,y,yerr = rand(3,10)\n                errorbar(x, y, yerr, marker='s', mfc='red',\n                         mec='green', ms=20, mew=4)\n\n            where mfc, mec, ms and mew are aliases for the longer\n            property names, markerfacecolor, markeredgecolor, markersize\n            and markeredgewidth.\n\n            Valid kwargs for the marker properties are\n\n            %(Line2D)s\n\n        Notes\n        -----\n        Error bars with negative values will not be shown when plotted on a\n        logarithmic axis.\n        "
    kwargs = cbook.normalize_kwargs(kwargs, _alias_map)
    kwargs = {k: v for (k, v) in kwargs.items() if (v is not None)}
    kwargs.setdefault('zorder', 2)
    if (errorevery < 1):
        raise ValueError('errorevery has to be a strictly positive integer')
    self._process_unit_info(xdata=x, ydata=y, kwargs=kwargs)
    if (not self._hold):
        self.cla()
    holdstate = self._hold
    self._hold = True
    if (fmt is None):
        fmt = 'none'
        msg = (('Use of None object as fmt keyword argument to ' + 'suppress plotting of data values is deprecated ') + 'since 1.4; use the string "none" instead.')
        warnings.warn(msg, mplDeprecation, stacklevel=1)
    plot_line = (fmt.lower() != 'none')
    label = kwargs.pop('label', None)
    fmt_style_kwargs = {k: v for (k, v) in zip(('linestyle', 'marker', 'color'), _process_plot_format(fmt)) if (v is not None)}
    if (fmt == 'none'):
        fmt_style_kwargs.pop('color')
    if (('color' in kwargs) or ('color' in fmt_style_kwargs) or (ecolor is not None)):
        base_style = {
            
        }
        if ('color' in kwargs):
            base_style['color'] = kwargs.pop('color')
    else:
        base_style = six.next(self._get_lines.prop_cycler)
    base_style['label'] = '_nolegend_'
    base_style.update(fmt_style_kwargs)
    if ('color' not in base_style):
        base_style['color'] = 'C0'
    if (ecolor is None):
        ecolor = base_style['color']
    if (not iterable(x)):
        x = [x]
    if (not iterable(y)):
        y = [y]
    if (xerr is not None):
        if (not iterable(xerr)):
            xerr = ([xerr] * len(x))
    if (yerr is not None):
        if (not iterable(yerr)):
            yerr = ([yerr] * len(y))
    plot_line_style = dict(base_style)
    plot_line_style.update(**kwargs)
    if barsabove:
        plot_line_style['zorder'] = (kwargs['zorder'] - 0.1)
    else:
        plot_line_style['zorder'] = (kwargs['zorder'] + 0.1)
    eb_lines_style = dict(base_style)
    eb_lines_style.pop('marker', None)
    eb_lines_style.pop('linestyle', None)
    eb_lines_style['color'] = ecolor
    if elinewidth:
        eb_lines_style['linewidth'] = elinewidth
    elif ('linewidth' in kwargs):
        eb_lines_style['linewidth'] = kwargs['linewidth']
    for key in ('transform', 'alpha', 'zorder', 'rasterized'):
        if (key in kwargs):
            eb_lines_style[key] = kwargs[key]
    eb_cap_style = dict(base_style)
    eb_cap_style.pop('marker', None)
    eb_cap_style.pop('ls', None)
    eb_cap_style['linestyle'] = 'none'
    if (capsize is None):
        capsize = rcParams['errorbar.capsize']
    if (capsize > 0):
        eb_cap_style['markersize'] = (2.0 * capsize)
    if (capthick is not None):
        eb_cap_style['markeredgewidth'] = capthick
    for key in ('markeredgewidth', 'transform', 'alpha', 'zorder', 'rasterized'):
        if (key in kwargs):
            eb_cap_style[key] = kwargs[key]
    eb_cap_style['color'] = ecolor
    data_line = None
    if plot_line:
        data_line = mlines.Line2D(x, y, **plot_line_style)
        self.add_line(data_line)
    barcols = []
    caplines = []

    def _bool_asarray_helper(d, expected):
        if (not iterable(d)):
            return np.asarray(([d] * expected), bool)
        else:
            return np.asarray(d, bool)
    lolims = _bool_asarray_helper(lolims, len(x))
    uplims = _bool_asarray_helper(uplims, len(x))
    xlolims = _bool_asarray_helper(xlolims, len(x))
    xuplims = _bool_asarray_helper(xuplims, len(x))
    everymask = ((np.arange(len(x)) % errorevery) == 0)

    def xywhere(xs, ys, mask):
        '\n            return xs[mask], ys[mask] where mask is True but xs and\n            ys are not arrays\n            '
        assert (len(xs) == len(ys))
        assert (len(xs) == len(mask))
        xs = [thisx for (thisx, b) in zip(xs, mask) if b]
        ys = [thisy for (thisy, b) in zip(ys, mask) if b]
        return (xs, ys)

    def extract_err(err, data):
        'private function to compute error bars\n\n            Parameters\n            ----------\n            err : iterable\n                xerr or yerr from errorbar\n            data : iterable\n                x or y from errorbar\n            '
        try:
            (a, b) = err
        except (TypeError, ValueError):
            pass
        else:
            if (iterable(a) and iterable(b)):
                low = [(thisx - thiserr) for (thisx, thiserr) in cbook.safezip(data, a)]
                high = [(thisx + thiserr) for (thisx, thiserr) in cbook.safezip(data, b)]
                return (low, high)
        if (len(err) > 1):
            fe = safe_first_element(err)
            if ((len(err) != len(data)) or (np.size(fe) > 1)):
                raise ValueError('err must be [ scalar | N, Nx1 or 2xN array-like ]')
        low = [(thisx - thiserr) for (thisx, thiserr) in cbook.safezip(data, err)]
        high = [(thisx + thiserr) for (thisx, thiserr) in cbook.safezip(data, err)]
        return (low, high)
    if (xerr is not None):
        (left, right) = extract_err(xerr, x)
        noxlims = (~ (xlolims | xuplims))
        if noxlims.any():
            (yo, _) = xywhere(y, right, (noxlims & everymask))
            (lo, ro) = xywhere(left, right, (noxlims & everymask))
            barcols.append(self.hlines(yo, lo, ro, **eb_lines_style))
            if (capsize > 0):
                caplines.append(mlines.Line2D(lo, yo, marker='|', **eb_cap_style))
                caplines.append(mlines.Line2D(ro, yo, marker='|', **eb_cap_style))
        if xlolims.any():
            (yo, _) = xywhere(y, right, (xlolims & everymask))
            (lo, ro) = xywhere(x, right, (xlolims & everymask))
            barcols.append(self.hlines(yo, lo, ro, **eb_lines_style))
            (rightup, yup) = xywhere(right, y, (xlolims & everymask))
            if self.xaxis_inverted():
                marker = mlines.CARETLEFTBASE
            else:
                marker = mlines.CARETRIGHTBASE
            caplines.append(mlines.Line2D(rightup, yup, ls='None', marker=marker, **eb_cap_style))
            if (capsize > 0):
                (xlo, ylo) = xywhere(x, y, (xlolims & everymask))
                caplines.append(mlines.Line2D(xlo, ylo, marker='|', **eb_cap_style))
        if xuplims.any():
            (yo, _) = xywhere(y, right, (xuplims & everymask))
            (lo, ro) = xywhere(left, x, (xuplims & everymask))
            barcols.append(self.hlines(yo, lo, ro, **eb_lines_style))
            (leftlo, ylo) = xywhere(left, y, (xuplims & everymask))
            if self.xaxis_inverted():
                marker = mlines.CARETRIGHTBASE
            else:
                marker = mlines.CARETLEFTBASE
            caplines.append(mlines.Line2D(leftlo, ylo, ls='None', marker=marker, **eb_cap_style))
            if (capsize > 0):
                (xup, yup) = xywhere(x, y, (xuplims & everymask))
                caplines.append(mlines.Line2D(xup, yup, marker='|', **eb_cap_style))
    if (yerr is not None):
        (lower, upper) = extract_err(yerr, y)
        noylims = (~ (lolims | uplims))
        if noylims.any():
            (xo, _) = xywhere(x, lower, (noylims & everymask))
            (lo, uo) = xywhere(lower, upper, (noylims & everymask))
            barcols.append(self.vlines(xo, lo, uo, **eb_lines_style))
            if (capsize > 0):
                caplines.append(mlines.Line2D(xo, lo, marker='_', **eb_cap_style))
                caplines.append(mlines.Line2D(xo, uo, marker='_', **eb_cap_style))
        if lolims.any():
            (xo, _) = xywhere(x, lower, (lolims & everymask))
            (lo, uo) = xywhere(y, upper, (lolims & everymask))
            barcols.append(self.vlines(xo, lo, uo, **eb_lines_style))
            (xup, upperup) = xywhere(x, upper, (lolims & everymask))
            if self.yaxis_inverted():
                marker = mlines.CARETDOWNBASE
            else:
                marker = mlines.CARETUPBASE
            caplines.append(mlines.Line2D(xup, upperup, ls='None', marker=marker, **eb_cap_style))
            if (capsize > 0):
                (xlo, ylo) = xywhere(x, y, (lolims & everymask))
                caplines.append(mlines.Line2D(xlo, ylo, marker='_', **eb_cap_style))
        if uplims.any():
            (xo, _) = xywhere(x, lower, (uplims & everymask))
            (lo, uo) = xywhere(lower, y, (uplims & everymask))
            barcols.append(self.vlines(xo, lo, uo, **eb_lines_style))
            (xlo, lowerlo) = xywhere(x, lower, (uplims & everymask))
            if self.yaxis_inverted():
                marker = mlines.CARETUPBASE
            else:
                marker = mlines.CARETDOWNBASE
            caplines.append(mlines.Line2D(xlo, lowerlo, ls='None', marker=marker, **eb_cap_style))
            if (capsize > 0):
                (xup, yup) = xywhere(x, y, (uplims & everymask))
                caplines.append(mlines.Line2D(xup, yup, marker='_', **eb_cap_style))
    for l in caplines:
        self.add_line(l)
    self.autoscale_view()
    self._hold = holdstate
    errorbar_container = ErrorbarContainer((data_line, tuple(caplines), tuple(barcols)), has_xerr=(xerr is not None), has_yerr=(yerr is not None), label=label)
    self.containers.append(errorbar_container)
    return errorbar_container