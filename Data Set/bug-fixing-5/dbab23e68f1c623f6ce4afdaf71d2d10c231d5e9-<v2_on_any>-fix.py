def v2_on_any(self, *args, **kwargs):
    self._display.display('--- play: {} task: {} ---'.format(getattr(self.play, 'name', None), self.task))
    self._display.display('     --- ARGS ')
    for (i, a) in enumerate(args):
        self._display.display(('     %s: %s' % (i, a)))
    self._display.display('      --- KWARGS ')
    for k in kwargs:
        self._display.display(('     %s: %s' % (k, kwargs[k])))