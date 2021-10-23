

def matshow(self, Z, **kwargs):
    "\n        Plot the values of a 2D matrix or array as color-coded image.\n\n        The matrix will be shown the way it would be printed, with the first\n        row at the top.  Row and column numbering is zero-based.\n\n        Parameters\n        ----------\n        Z : array-like(M, N)\n            The matrix to be displayed.\n\n        Returns\n        -------\n        image : `~matplotlib.image.AxesImage`\n\n        Other Parameters\n        ----------------\n        **kwargs : `~matplotlib.axes.Axes.imshow` arguments\n\n        See Also\n        --------\n        imshow : More general function to plot data on a 2D regular raster.\n\n        Notes\n        -----\n        This is just a convenience function wrapping `.imshow` to set useful\n        defaults for a displaying a matrix. In particular:\n\n        - Set ``origin='upper'``.\n        - Set ``interpolation='nearest'``.\n        - Set ``aspect='equal'``.\n        - Ticks are placed to the left and above.\n        - Ticks are formatted to show integer indices.\n\n        "
    Z = np.asanyarray(Z)
    kw = {
        'origin': 'upper',
        'interpolation': 'nearest',
        'aspect': 'equal',
        **kwargs,
    }
    im = self.imshow(Z, **kw)
    self.title.set_y(1.05)
    self.xaxis.tick_top()
    self.xaxis.set_ticks_position('both')
    self.xaxis.set_major_locator(mticker.MaxNLocator(nbins=9, steps=[1, 2, 5, 10], integer=True))
    self.yaxis.set_major_locator(mticker.MaxNLocator(nbins=9, steps=[1, 2, 5, 10], integer=True))
    return im
