

def on_open_shell(self):
    try:
        commands = ((((('{"command": "' + self._connection._play_context.remote_user) + '", "prompt": "Password:", "answer": "') + self._connection._play_context.password) + '"}'), '{"command": "config paging disable"}')
        for cmd in commands:
            self._exec_cli_command(cmd)
    except AnsibleConnectionFailure:
        try:
            self._exec_cli_command(b'config paging disable')
        except AnsibleConnectionFailure:
            raise AnsibleConnectionFailure('unable to set terminal parameters')
