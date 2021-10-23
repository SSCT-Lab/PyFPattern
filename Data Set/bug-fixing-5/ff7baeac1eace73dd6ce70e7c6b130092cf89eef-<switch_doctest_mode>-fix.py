def switch_doctest_mode(self, mode):
    'Switch prompts to classic for %doctest_mode'
    if mode:
        self._prompts_before = self.prompts
        self.prompts = ClassicPrompts(self)
    elif self._prompts_before:
        self.prompts = self._prompts_before
        self._prompts_before = None
    self._update_layout()