@ensure_connect
def open_shell(self):
    'Opens the vty shell on the connection'
    self._shell = self.ssh.invoke_shell()
    self._shell.settimeout(self._play_context.timeout)
    self.receive()
    if self._shell:
        self._terminal.on_open_shell()
    if getattr(self._play_context, 'become', None):
        auth_pass = self._play_context.become_pass
        self._terminal.on_authorize(passwd=auth_pass)