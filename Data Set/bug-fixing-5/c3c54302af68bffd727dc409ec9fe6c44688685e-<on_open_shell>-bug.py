def on_open_shell(self):
    try:
        for cmd in (b'disable clipaging', b'configure cli columns 256'):
            self._exec_cli_command(cmd)
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to set terminal parameters')