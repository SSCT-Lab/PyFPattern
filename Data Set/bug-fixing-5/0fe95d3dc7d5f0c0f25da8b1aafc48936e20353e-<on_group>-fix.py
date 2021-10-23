def on_group(self, *largs):
    super(CheckBox, self).on_group(*largs)
    if self.active:
        self._release_group(self)