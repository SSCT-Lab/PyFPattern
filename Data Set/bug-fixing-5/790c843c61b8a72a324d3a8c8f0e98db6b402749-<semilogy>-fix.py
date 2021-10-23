@docstring.dedent_interpd
def semilogy(self, *args, **kwargs):
    "\n        Make a plot with log scaling on the *y* axis.\n\n        Parameters\n        ----------\n        basey : float, optional\n            Base of the *y* logarithm. The scalar should be larger\n            than 1.\n\n        subsy : array_like, optional\n            The location of the minor yticks; *None* defaults to\n            autosubs, which depend on the number of decades in the\n            plot; see :meth:`~matplotlib.axes.Axes.set_yscale` for\n            details.\n\n        nonposy : string, optional, {'mask', 'clip'}\n            Non-positive values in *y* can be masked as\n            invalid, or clipped to a very small positive number.\n\n        Returns\n        -------\n        `~matplotlib.pyplot.plot`\n            Log-scaled plot on the *y* axis.\n\n        Other Parameters\n        ----------------\n        **kwargs :\n            Keyword arguments control the :class:`~matplotlib.lines.Line2D`\n            properties:\n\n            %(Line2D)s\n\n        Notes\n        -----\n        This function supports all the keyword arguments of\n        :func:`~matplotlib.pyplot.plot` and\n        :meth:`matplotlib.axes.Axes.set_yscale`.\n        "
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