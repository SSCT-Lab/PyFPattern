def on_collapse(self, instance, value):
    accordion = self.accordion
    if (accordion is None):
        return
    if (not value):
        self.accordion.select(self)
    collapse_alpha = float(value)
    if self._anim_collapse:
        self._anim_collapse.stop()
        self._anim_collapse = None
    if (self.collapse_alpha != collapse_alpha):
        self._anim_collapse = Animation(collapse_alpha=collapse_alpha, t=accordion.anim_func, d=accordion.anim_duration).start(self)