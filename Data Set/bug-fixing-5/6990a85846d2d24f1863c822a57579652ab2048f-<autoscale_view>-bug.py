def autoscale_view(self, tight=None, scalex=True, scaley=True, scalez=True):
    '\n        Autoscale the view limits using the data limits.\n        See :meth:`matplotlib.axes.Axes.autoscale_view` for documentation.\n        Note that this function applies to the 3D axes, and as such\n        adds the *scalez* to the function arguments.\n\n        .. versionchanged :: 1.1.0\n            Function signature was changed to better match the 2D version.\n            *tight* is now explicitly a kwarg and placed first.\n\n        .. versionchanged :: 1.2.1\n            This is now fully functional.\n\n        '
    if (not self._ready):
        return
    if (tight is None):
        _tight = (self._tight or ((len(self.images) > 0) and (len(self.lines) == len(self.patches) == 0)))
    else:
        _tight = self._tight = bool(tight)
    if (scalex and self._autoscaleXon):
        self._shared_x_axes.clean()
        (x0, x1) = self.xy_dataLim.intervalx
        xlocator = self.xaxis.get_major_locator()
        (x0, x1) = xlocator.nonsingular(x0, x1)
        if (self._xmargin > 0):
            delta = ((x1 - x0) * self._xmargin)
            x0 -= delta
            x1 += delta
        if (not _tight):
            (x0, x1) = xlocator.view_limits(x0, x1)
        self.set_xbound(x0, x1)
    if (scaley and self._autoscaleYon):
        self._shared_y_axes.clean()
        (y0, y1) = self.xy_dataLim.intervaly
        ylocator = self.yaxis.get_major_locator()
        (y0, y1) = ylocator.nonsingular(y0, y1)
        if (self._ymargin > 0):
            delta = ((y1 - y0) * self._ymargin)
            y0 -= delta
            y1 += delta
        if (not _tight):
            (y0, y1) = ylocator.view_limits(y0, y1)
        self.set_ybound(y0, y1)
    if (scalez and self._autoscaleZon):
        self._shared_z_axes.clean()
        (z0, z1) = self.zz_dataLim.intervalx
        zlocator = self.zaxis.get_major_locator()
        (z0, z1) = zlocator.nonsingular(z0, z1)
        if (self._zmargin > 0):
            delta = ((z1 - z0) * self._zmargin)
            z0 -= delta
            z1 += delta
        if (not _tight):
            (z0, z1) = zlocator.view_limits(z0, z1)
        self.set_zbound(z0, z1)