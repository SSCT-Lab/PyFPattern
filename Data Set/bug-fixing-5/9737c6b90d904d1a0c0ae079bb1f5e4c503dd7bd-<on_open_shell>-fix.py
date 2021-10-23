def on_open_shell(self):
    try:
        for cmd in (b'set terminal length 0', b'set terminal width 512'):
            self._exec_cli_command(cmd)
        self._exec_cli_command((b'set terminal length %d' % self.terminal_length))
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to set terminal parameters')