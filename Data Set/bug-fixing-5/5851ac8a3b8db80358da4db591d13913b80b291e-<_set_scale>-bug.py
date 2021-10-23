def _set_scale(self):
    '\n        Check if parent has set its scale\n        '
    if (self._orientation == 'x'):
        pscale = self._parent.xaxis.get_scale()
        set_scale = self.set_xscale
    if (self._orientation == 'y'):
        pscale = self._parent.yaxis.get_scale()
        set_scale = self.set_yscale
    if (pscale == self._parentscale):
        return
    else:
        self._parentscale = pscale
    if (pscale == 'log'):
        defscale = 'functionlog'
    else:
        defscale = 'function'
    if self._ticks_set:
        ticks = self._axis.get_ticklocs()
    set_scale(defscale, functions=self._functions)
    if self._ticks_set:
        self._axis.set_major_locator(FixedLocator(ticks))