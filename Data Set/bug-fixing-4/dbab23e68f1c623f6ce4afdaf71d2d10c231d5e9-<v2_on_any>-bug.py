def v2_on_any(self, *args, **kwargs):
    i = 0
    if self.play:
        play_str = ('play: %s' % self.play.name)
    if self.task:
        task_str = ('task: %s' % self.task)
    self._display.display(('--- %s %s ---' % (self.play_str, self.task_str)))
    self._display.display('     --- ARGS ')
    for a in args:
        self._display.display(('     %s: %s' % (i, a)))
        i += 1
    self._display.display('      --- KWARGS ')
    for k in kwargs:
        self._display.display(('     %s: %s' % (k, kwargs[k])))