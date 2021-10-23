def set_markevery(self, every):
    'Set the markevery property to subsample the plot when using markers.\n\n        e.g., if `every=5`, every 5-th marker will be plotted.\n\n        ACCEPTS: [None | int | length-2 tuple of int | slice |\n        list/array of int | float | length-2 tuple of float]\n\n        Parameters\n        ----------\n        every: None | int | length-2 tuple of int | slice | list/array of int | float | length-2 tuple of float\n            Which markers to plot.\n\n            - every=None, every point will be plotted.\n            - every=N, every N-th marker will be plotted starting with\n              marker 0.\n            - every=(start, N), every N-th marker, starting at point\n              start, will be plotted.\n            - every=slice(start, end, N), every N-th marker, starting at\n              point start, upto but not including point end, will be plotted.\n            - every=[i, j, m, n], only markers at points i, j, m, and n\n              will be plotted.\n            - every=0.1, (i.e. a float) then markers will be spaced at\n              approximately equal distances along the line; the distance\n              along the line between markers is determined by multiplying the\n              display-coordinate distance of the axes bounding-box diagonal\n              by the value of every.\n            - every=(0.5, 0.1) (i.e. a length-2 tuple of float), the\n              same functionality as every=0.1 is exhibited but the first\n              marker will be 0.5 multiplied by the\n              display-cordinate-diagonal-distance along the line.\n\n        Notes\n        -----\n        Setting the markevery property will only show markers at actual data\n        points.  When using float arguments to set the markevery property\n        on irregularly spaced data, the markers will likely not appear evenly\n        spaced because the actual data points do not coincide with the\n        theoretical spacing between markers.\n\n        When using a start offset to specify the first marker, the offset will\n        be from the first data point which may be different from the first\n        the visible data point if the plot is zoomed in.\n\n        If zooming in on a plot when using float arguments then the actual\n        data points that have markers will change because the distance between\n        markers is always determined from the display-coordinates\n        axes-bounding-box-diagonal regardless of the actual axes data limits.\n\n        '
    if (self._markevery != every):
        self.stale = True
    self._markevery = every