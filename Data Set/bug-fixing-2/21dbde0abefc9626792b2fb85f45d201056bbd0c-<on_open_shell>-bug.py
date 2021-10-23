

def on_open_shell(self):
    if self._get_prompt().endswith(b'#'):
        self.disable_pager()
