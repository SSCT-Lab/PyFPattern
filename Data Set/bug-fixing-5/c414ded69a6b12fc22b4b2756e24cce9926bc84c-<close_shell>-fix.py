def close_shell(self):
    if self._shell:
        self._terminal.on_close_shell()
    if (self._terminal.supports_multiplexing and self._shell):
        self._shell.close()
        self._shell = None
    return (0, 'shell closed', '')