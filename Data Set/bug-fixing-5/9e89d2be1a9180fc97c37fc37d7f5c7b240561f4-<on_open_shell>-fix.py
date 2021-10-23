def on_open_shell(self):
    try:
        self._exec_cli_command(b'modify cli preference display-threshold 0 pager disabled')
    except AnsibleConnectionFailure as ex:
        output = str(ex)
        if ('modify: command not found' in output):
            try:
                self._exec_cli_command(b'tmsh modify cli preference display-threshold 0 pager disabled')
            except AnsibleConnectionFailure as ex:
                raise AnsibleConnectionFailure('unable to set terminal parameters')