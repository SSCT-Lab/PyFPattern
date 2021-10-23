

@unpack_labeled_data(replace_names=['x', 'y', 's', 'linewidths', 'edgecolors', 'c', 'facecolor', 'facecolors', 'color'], label_namer='y')
@docstring.dedent_interpd
def scatter(self, x, y, s=20, c=None, marker='o', cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, edgecolors=None, **kwargs):
    "\n        Make a scatter plot of x vs y, where x and y are sequence like objects\n        of the same length.\n\n        Parameters\n        ----------\n        x, y : array_like, shape (n, )\n            Input data\n\n        s : scalar or array_like, shape (n, ), optional, default: 20\n            size in points^2.\n\n        c : color, sequence, or sequence of color, optional, default: 'b'\n            `c` can be a single color format string, or a sequence of color\n            specifications of length `N`, or a sequence of `N` numbers to be\n            mapped to colors using the `cmap` and `norm` specified via kwargs\n            (see below). Note that `c` should not be a single numeric RGB or\n            RGBA sequence because that is indistinguishable from an array of\n            values to be colormapped.  `c` can be a 2-D array in which the\n            rows are RGB or RGBA, however, including the case of a single\n            row to specify the same color for all points.\n\n        marker : `~matplotlib.markers.MarkerStyle`, optional, default: 'o'\n            See `~matplotlib.markers` for more information on the different\n            styles of markers scatter supports. `marker` can be either\n            an instance of the class or the text shorthand for a particular\n            marker.\n\n        cmap : `~matplotlib.colors.Colormap`, optional, default: None\n            A `~matplotlib.colors.Colormap` instance or registered name.\n            `cmap` is only used if `c` is an array of floats. If None,\n            defaults to rc `image.cmap`.\n\n        norm : `~matplotlib.colors.Normalize`, optional, default: None\n            A `~matplotlib.colors.Normalize` instance is used to scale\n            luminance data to 0, 1. `norm` is only used if `c` is an array of\n            floats. If `None`, use the default :func:`normalize`.\n\n        vmin, vmax : scalar, optional, default: None\n            `vmin` and `vmax` are used in conjunction with `norm` to normalize\n            luminance data.  If either are `None`, the min and max of the\n            color array is used.  Note if you pass a `norm` instance, your\n            settings for `vmin` and `vmax` will be ignored.\n\n        alpha : scalar, optional, default: None\n            The alpha blending value, between 0 (transparent) and 1 (opaque)\n\n        linewidths : scalar or array_like, optional, default: None\n            If None, defaults to (lines.linewidth,).\n\n        edgecolors : color or sequence of color, optional, default: None\n            If None, defaults to (patch.edgecolor).\n            If 'face', the edge color will always be the same as\n            the face color.  If it is 'none', the patch boundary will not\n            be drawn.  For non-filled markers, the `edgecolors` kwarg\n            is ignored; color is determined by `c`.\n\n        Returns\n        -------\n        paths : `~matplotlib.collections.PathCollection`\n\n        Other parameters\n        ----------------\n        kwargs : `~matplotlib.collections.Collection` properties\n\n        Notes\n        ------\n        Any or all of `x`, `y`, `s`, and `c` may be masked arrays, in\n        which case all masks will be combined and only unmasked points\n        will be plotted.\n\n        Fundamentally, scatter works with 1-D arrays; `x`, `y`, `s`,\n        and `c` may be input as 2-D arrays, but within scatter\n        they will be flattened. The exception is `c`, which\n        will be flattened only if its size matches the size of `x`\n        and `y`.\n\n        Examples\n        --------\n        .. plot:: mpl_examples/shapes_and_collections/scatter_demo.py\n\n        "
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
            mcolors.colorConverter.to_rgba_array(co)
        except ValueError:
            raise ValueError("'color' kwarg must be an mpl color spec or sequence of color specs.\nFor a sequence of values to be color-mapped, use the 'c' kwarg instead.")
        if (edgecolors is None):
            edgecolors = co
        if (facecolors is None):
            facecolors = co
    if (c is None):
        if (facecolors is not None):
            c = facecolors
        else:
            c = 'b'
    self._process_unit_info(xdata=x, ydata=y, kwargs=kwargs)
    x = self.convert_xunits(x)
    y = self.convert_yunits(y)
    x = np.ma.ravel(x)
    y = np.ma.ravel(y)
    if (x.size != y.size):
        raise ValueError('x and y must be the same size')
    s = np.ma.ravel(s)
    try:
        c_array = np.asanyarray(c, dtype=float)
        if (c_array.size == x.size):
            c = np.ma.ravel(c_array)
        else:
            c_array = None
    except ValueError:
        c_array = None
    if (c_array is None):
        colors = c
    else:
        colors = None
    (x, y, s, c) = cbook.delete_masked_points(x, y, s, c)
    scales = s
    if ((marker is None) and (not (verts is None))):
        marker = (verts, 0)
        verts = None
    if isinstance(marker, mmarkers.MarkerStyle):
        marker_obj = marker
    else:
        marker_obj = mmarkers.MarkerStyle(marker)
    path = marker_obj.get_path().transformed(marker_obj.get_transform())
    if (not marker_obj.is_filled()):
        edgecolors = 'face'
    offsets = np.dstack((x, y))
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
    if ((self._xmargin < 0.05) and (x.size > 0)):
        self.set_xmargin(0.05)
    if ((self._ymargin < 0.05) and (x.size > 0)):
        self.set_ymargin(0.05)
    self.add_collection(collection)
    self.autoscale_view()
    return collection
