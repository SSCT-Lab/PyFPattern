def on_open_shell(self):
    if self._get_prompt().strip().endswith(b'#'):
        self.disable_pager()