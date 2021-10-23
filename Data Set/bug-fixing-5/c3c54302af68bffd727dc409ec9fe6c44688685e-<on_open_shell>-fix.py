def on_open_shell(self):
    try:
        self._exec_cli_command(b'disable clipaging')
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to set terminal parameters')
    try:
        self._exec_cli_command(b'configure cli columns 256')
    except AnsibleConnectionFailure:
        self._connection.queue_message('warning', 'Unable to configure cli columns, command responses may be truncated')