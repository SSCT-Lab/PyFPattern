

@_preprocess_data(replace_names=['x', 'y', 's', 'linewidths', 'edgecolors', 'c', 'facecolor', 'facecolors', 'color'], label_namer='y')
def scatter(self, x, y, s=None, c=None, marker=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, edgecolors=None, **kwargs):
    "\n        Make a scatter plot of `x` vs `y`\n\n        Marker size is scaled by `s` and marker color is mapped to `c`\n\n        Parameters\n        ----------\n        x, y : array_like, shape (n, )\n            Input data\n\n        s : scalar or array_like, shape (n, ), optional\n            size in points^2.  Default is `rcParams['lines.markersize'] ** 2`.\n\n        c : color, sequence, or sequence of color, optional, default: 'b'\n            `c` can be a single color format string, or a sequence of color\n            specifications of length `N`, or a sequence of `N` numbers to be\n            mapped to colors using the `cmap` and `norm` specified via kwargs\n            (see below). Note that `c` should not be a single numeric RGB or\n            RGBA sequence because that is indistinguishable from an array of\n            values to be colormapped.  `c` can be a 2-D array in which the\n            rows are RGB or RGBA, however, including the case of a single\n            row to specify the same color for all points.\n\n        marker : `~matplotlib.markers.MarkerStyle`, optional, default: 'o'\n            See `~matplotlib.markers` for more information on the different\n            styles of markers scatter supports. `marker` can be either\n            an instance of the class or the text shorthand for a particular\n            marker.\n\n        cmap : `~matplotlib.colors.Colormap`, optional, default: None\n            A `~matplotlib.colors.Colormap` instance or registered name.\n            `cmap` is only used if `c` is an array of floats. If None,\n            defaults to rc `image.cmap`.\n\n        norm : `~matplotlib.colors.Normalize`, optional, default: None\n            A `~matplotlib.colors.Normalize` instance is used to scale\n            luminance data to 0, 1. `norm` is only used if `c` is an array of\n            floats. If `None`, use the default :func:`normalize`.\n\n        vmin, vmax : scalar, optional, default: None\n            `vmin` and `vmax` are used in conjunction with `norm` to normalize\n            luminance data.  If either are `None`, the min and max of the\n            color array is used.  Note if you pass a `norm` instance, your\n            settings for `vmin` and `vmax` will be ignored.\n\n        alpha : scalar, optional, default: None\n            The alpha blending value, between 0 (transparent) and 1 (opaque)\n\n        linewidths : scalar or array_like, optional, default: None\n            If None, defaults to (lines.linewidth,).\n\n        verts : sequence of (x, y), optional\n            If `marker` is None, these vertices will be used to\n            construct the marker.  The center of the marker is located\n            at (0,0) in normalized units.  The overall marker is rescaled\n            by ``s``.\n\n        edgecolors : color or sequence of color, optional, default: None\n            If None, defaults to 'face'\n\n            If 'face', the edge color will always be the same as\n            the face color.\n\n            If it is 'none', the patch boundary will not\n            be drawn.\n\n            For non-filled markers, the `edgecolors` kwarg\n            is ignored and forced to 'face' internally.\n\n        Returns\n        -------\n        paths : `~matplotlib.collections.PathCollection`\n\n        Other parameters\n        ----------------\n        kwargs : `~matplotlib.collections.Collection` properties\n\n        See Also\n        --------\n        plot : to plot scatter plots when markers are identical in size and\n            color\n\n        Notes\n        -----\n\n        * The `plot` function will be faster for scatterplots where markers\n          don't vary in size or color.\n\n        * Any or all of `x`, `y`, `s`, and `c` may be masked arrays, in which\n          case all masks will be combined and only unmasked points will be\n          plotted.\n\n          Fundamentally, scatter works with 1-D arrays; `x`, `y`, `s`, and `c`\n          may be input as 2-D arrays, but within scatter they will be\n          flattened. The exception is `c`, which will be flattened only if its\n          size matches the size of `x` and `y`.\n\n        "
    if (not self._hold):
        self.cla()
    facecolors = None
    edgecolors = kwargs.pop('edgecolor', edgecolors)
    fc = kwargs.pop('facecolors', None)
    fc = kwargs.pop('facecolor', fc)
    if (fc is not None):
        facecolors = fc
    co = kwargs.pop('color', None)
    if (co is not None):
        try:
            mcolors.to_rgba_array(co)
        except ValueError:
            raise ValueError("'color' kwarg must be an mpl color spec or sequence of color specs.\nFor a sequence of values to be color-mapped, use the 'c' kwarg instead.")
        if (edgecolors is None):
            edgecolors = co
        if (facecolors is None):
            facecolors = co
        if (c is not None):
            raise ValueError("Supply a 'c' kwarg or a 'color' kwarg but not both; they differ but their functionalities overlap.")
    if (c is None):
        if (facecolors is not None):
            c = facecolors
        elif rcParams['_internal.classic_mode']:
            c = 'b'
        else:
            c = self._get_patches_for_fill.get_next_color()
        c_none = True
    else:
        c_none = False
    if ((edgecolors is None) and (not rcParams['_internal.classic_mode'])):
        edgecolors = 'face'
    self._process_unit_info(xdata=x, ydata=y, kwargs=kwargs)
    x = self.convert_xunits(x)
    y = self.convert_yunits(y)
    xy_shape = (np.shape(x), np.shape(y))
    x = np.ma.ravel(x)
    y = np.ma.ravel(y)
    if (x.size != y.size):
        raise ValueError('x and y must be the same size')
    if (s is None):
        if rcParams['_internal.classic_mode']:
            s = 20
        else:
            s = (rcParams['lines.markersize'] ** 2.0)
    s = np.ma.ravel(s)
    if (c_none or (co is not None)):
        c_array = None
    else:
        try:
            c_array = np.asanyarray(c, dtype=float)
            if (c_array.shape in xy_shape):
                c = np.ma.ravel(c_array)
            else:
                c_array = None
        except ValueError:
            c_array = None
    if (c_array is None):
        try:
            colors = mcolors.to_rgba_array(c)
        except ValueError:
            msg = 'c of shape {0} not acceptable as a color sequence for x with size {1}, y with size {2}'
            raise ValueError(msg.format(c.shape, x.size, y.size))
    else:
        colors = None
    (x, y, s, c, colors, edgecolors, linewidths) = cbook.delete_masked_points(x, y, s, c, colors, edgecolors, linewidths)
    scales = s
    if ((marker is None) and (verts is not None)):
        marker = (verts, 0)
        verts = None
    if (marker is None):
        marker = rcParams['scatter.marker']
    if isinstance(marker, mmarkers.MarkerStyle):
        marker_obj = marker
    else:
        marker_obj = mmarkers.MarkerStyle(marker)
    path = marker_obj.get_path().transformed(marker_obj.get_transform())
    if (not marker_obj.is_filled()):
        edgecolors = 'face'
        linewidths = rcParams['lines.linewidth']
    offsets = np.column_stack([x, y])
    collection = mcoll.PathCollection((path,), scales, facecolors=colors, edgecolors=edgecolors, linewidths=linewidths, offsets=offsets, transOffset=kwargs.pop('transform', self.transData), alpha=alpha)
    collection.set_transform(mtransforms.IdentityTransform())
    collection.update(kwargs)
    if (colors is None):
        if ((norm is not None) and (not isinstance(norm, mcolors.Normalize))):
            msg = "'norm' must be an instance of 'mcolors.Normalize'"
            raise ValueError(msg)
        collection.set_array(np.asarray(c))
        collection.set_cmap(cmap)
        collection.set_norm(norm)
        if ((vmin is not None) or (vmax is not None)):
            collection.set_clim(vmin, vmax)
        else:
            collection.autoscale_None()
    if rcParams['_internal.classic_mode']:
        if ((self._xmargin < 0.05) and (x.size > 0)):
            self.set_xmargin(0.05)
        if ((self._ymargin < 0.05) and (x.size > 0)):
            self.set_ymargin(0.05)
    self.add_collection(collection)
    self.autoscale_view()
    return collection
