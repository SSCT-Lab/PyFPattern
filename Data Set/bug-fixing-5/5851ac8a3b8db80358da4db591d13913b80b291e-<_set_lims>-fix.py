def _set_lims(self):
    '\n        Set the limits based on parent limits and the convert method\n        between the parent and this secondary axes.\n        '
    if (self._orientation == 'x'):
        lims = self._parent.get_xlim()
        set_lim = self.set_xlim
    if (self._orientation == 'y'):
        lims = self._parent.get_ylim()
        set_lim = self.set_ylim
    order = (lims[0] < lims[1])
    lims = self._functions[0](np.array(lims))
    neworder = (lims[0] < lims[1])
    if (neworder != order):
        lims = lims[::(- 1)]
    set_lim(lims)