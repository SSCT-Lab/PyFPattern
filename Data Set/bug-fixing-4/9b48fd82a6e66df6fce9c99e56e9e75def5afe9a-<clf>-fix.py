def clf(self, keep_observers=False):
    '\n        Clear the figure.\n\n        Set *keep_observers* to True if, for example,\n        a gui widget is tracking the axes in the figure.\n        '
    self.suppressComposite = None
    self.callbacks = cbook.CallbackRegistry()
    for ax in tuple(self.axes):
        ax.cla()
        self.delaxes(ax)
    toolbar = getattr(self.canvas, 'toolbar', None)
    if (toolbar is not None):
        toolbar.update()
    self._axstack.clear()
    self.artists = []
    self.lines = []
    self.patches = []
    self.texts = []
    self.images = []
    self.legends = []
    if (not keep_observers):
        self._axobservers = []
    self._suptitle = None
    if self.get_constrained_layout():
        layoutbox.nonetree(self._layoutbox)
    self.stale = True