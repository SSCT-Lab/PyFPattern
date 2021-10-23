def on_open_shell(self):
    try:
        for cmd in (b'terminal length 0', b'terminal width 512'):
            self._exec_cli_command(cmd)
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to set terminal parameters')