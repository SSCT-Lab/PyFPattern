@docstring.dedent_interpd
def axhline(self, y=0, xmin=0, xmax=1, **kwargs):
    "\n        Add a horizontal line across the axis.\n\n        Parameters\n        ----------\n        y : scalar, optional, default: 0\n            y position in data coordinates of the horizontal line.\n\n        xmin : scalar, optional, default: 0\n            Should be between 0 and 1, 0 being the far left of the plot, 1 the\n            far right of the plot.\n\n        xmax : scalar, optional, default: 1\n            Should be between 0 and 1, 0 being the far left of the plot, 1 the\n            far right of the plot.\n\n        Returns\n        -------\n        :class:`~matplotlib.lines.Line2D`\n\n        Notes\n        -----\n        kwargs are passed to :class:`~matplotlib.lines.Line2D` and can be used\n        to control the line properties.\n\n        Examples\n        --------\n\n        * draw a thick red hline at 'y' = 0 that spans the xrange::\n\n            >>> axhline(linewidth=4, color='r')\n\n        * draw a default hline at 'y' = 1 that spans the xrange::\n\n            >>> axhline(y=1)\n\n        * draw a default hline at 'y' = .5 that spans the middle half of\n          the xrange::\n\n            >>> axhline(y=.5, xmin=0.25, xmax=0.75)\n\n        Valid kwargs are :class:`~matplotlib.lines.Line2D` properties,\n        with the exception of 'transform':\n\n        %(Line2D)s\n\n        See also\n        --------\n        hline : add horizontal lines in data coordinates\n        axhspan : add a horizontal span (rectangle) across the axis\n        "
    if ('transform' in kwargs):
        raise ValueError(("'transform' is not allowed as a kwarg;" + 'axhline generates its own transform.'))
    (ymin, ymax) = self.get_ybound()
    self._process_unit_info(ydata=y, kwargs=kwargs)
    yy = self.convert_yunits(y)
    scaley = ((yy < ymin) or (yy > ymax))
    trans = self.get_yaxis_transform(which='grid')
    l = mlines.Line2D([xmin, xmax], [y, y], transform=trans, **kwargs)
    self.add_line(l)
    self.autoscale_view(scalex=False, scaley=scaley)
    return l