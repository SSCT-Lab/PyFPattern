def on_open_shell(self):
    try:
        for c in ['set cli timestamp disable', 'set cli screen-length 0']:
            self._exec_cli_command(c)
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to set terminal parameters')