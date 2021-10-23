def set_markeredgecolor(self, ec):
    '\n        Set the marker edge color\n\n        ACCEPTS: any matplotlib color\n        '
    if (ec is None):
        ec = 'auto'
    if ((self._markeredgecolor is None) or (self._markeredgecolor != ec)):
        self.stale = True
    self._markeredgecolor = ec