def set_ticks(self, ticks, minor=False):
    '\n        Set the x ticks with list of *ticks*\n\n        Parameters\n        ----------\n        ticks : list\n            List of x-axis tick locations.\n\n        minor : bool, optional\n            If ``False`` sets major ticks, if ``True`` sets minor ticks.\n            Default is ``False``.\n        '
    ret = self._axis.set_ticks(ticks, minor=minor)
    self.stale = True
    self._ticks_set = True
    return ret