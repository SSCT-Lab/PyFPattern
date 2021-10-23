def open_shell(self, timeout=10):
    self._shell = self.ssh.invoke_shell()
    self._shell.settimeout(self._play_context.timeout)
    self.receive()
    if self._shell:
        self._terminal.on_open_shell()
    if hasattr(self._play_context, 'become'):
        if self._play_context.become:
            auth_pass = self._play_context.become_pass
            self._terminal.on_authorize(passwd=auth_pass)