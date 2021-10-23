def on_open_shell(self):
    try:
        self._exec_cli_command(b'terminal length 0')
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to set terminal parameters')
    try:
        self._exec_cli_command(b'terminal width 512')
    except AnsibleConnectionFailure:
        display.display('WARNING: Unable to set terminal width, command responses may be truncated')