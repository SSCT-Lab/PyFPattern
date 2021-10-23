@docstring.dedent_interpd
def axvline(self, x=0, ymin=0, ymax=1, **kwargs):
    "\n        Add a vertical line across the axes.\n\n        Parameters\n        ----------\n        x : scalar, optional, default: 0\n            x position in data coordinates of the vertical line.\n\n        ymin : scalar, optional, default: 0\n            Should be between 0 and 1, 0 being the bottom of the plot, 1 the\n            top of the plot.\n\n        ymax : scalar, optional, default: 1\n            Should be between 0 and 1, 0 being the bottom of the plot, 1 the\n            top of the plot.\n\n        Returns\n        -------\n        :class:`~matplotlib.lines.Line2D`\n\n\n        Examples\n        --------\n        * draw a thick red vline at *x* = 0 that spans the yrange::\n\n            >>> axvline(linewidth=4, color='r')\n\n        * draw a default vline at *x* = 1 that spans the yrange::\n\n            >>> axvline(x=1)\n\n        * draw a default vline at *x* = .5 that spans the middle half of\n          the yrange::\n\n            >>> axvline(x=.5, ymin=0.25, ymax=0.75)\n\n        Valid kwargs are :class:`~matplotlib.lines.Line2D` properties,\n        with the exception of 'transform':\n\n        %(Line2D)s\n\n        See also\n        --------\n        vlines : add vertical lines in data coordinates\n        axvspan : add a vertical span (rectangle) across the axis\n        "
    if ('transform' in kwargs):
        raise ValueError(("'transform' is not allowed as a kwarg;" + 'axvline generates its own transform.'))
    (xmin, xmax) = self.get_xbound()
    self._process_unit_info(xdata=x, kwargs=kwargs)
    xx = self.convert_xunits(x)
    scalex = ((xx < xmin) or (xx > xmax))
    trans = self.get_xaxis_transform(which='grid')
    l = mlines.Line2D([x, x], [ymin, ymax], transform=trans, **kwargs)
    self.add_line(l)
    self.autoscale_view(scalex=scalex, scaley=False)
    return l