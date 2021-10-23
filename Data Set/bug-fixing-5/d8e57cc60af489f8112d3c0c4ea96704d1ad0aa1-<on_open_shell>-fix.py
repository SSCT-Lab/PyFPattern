def on_open_shell(self):
    try:
        prompt = self._get_prompt()
        if prompt.strip().endswith('%'):
            display.vvv('starting cli', self._connection._play_context.remote_addr)
            self._exec_cli_command('cli')
        for c in ['set cli timestamp disable', 'set cli screen-length 0']:
            self._exec_cli_command(c)
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to set terminal parameters')