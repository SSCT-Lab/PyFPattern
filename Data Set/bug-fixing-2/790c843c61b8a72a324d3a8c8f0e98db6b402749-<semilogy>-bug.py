

@docstring.dedent_interpd
def semilogy(self, *args, **kwargs):
    "Make a plot with log scaling on the `y` axis.\n\n        Parameters\n        ----------\n        basey : scalar > 1\n            Base of the `y` logarithm.\n\n        subsy : None or iterable\n            The location of the minor yticks. None defaults to\n            autosubs, which depend on the number of decades in the\n            plot. See :meth:`~matplotlib.axes.Axes.set_yscale` for\n            details.\n\n        nonposy : {'mask' | 'clip'} str\n            Non-positive values in `y` can be masked as\n            invalid, or clipped to a very small positive number.\n\n        Returns\n        -------\n        `~matplotlib.lines.Line2D`\n            Line instance of the plot.\n\n        Other Parameters\n        ----------------\n        **kwargs :\n            This function supports all the keyword arguments of\n            :func:`~matplotlib.pyplot.plot` and\n            :meth:`matplotlib.axes.Axes.set_xscale`.\n\n            Keyword arguments also control the\n            :class:`~matplotlib.lines.Line2D` properties:\n\n            %(Line2D)s\n        "
    if (not self._hold):
        self.cla()
    d = {
        'basey': kwargs.pop('basey', 10),
        'subsy': kwargs.pop('subsy', None),
    }
    self.set_yscale('log', **d)
    b = self._hold
    self._hold = True
    l = self.plot(*args, **kwargs)
    self._hold = b
    return l
