def on_group(self, *largs):
    super().on_group(*largs)
    if self.active:
        self._release_group(self)