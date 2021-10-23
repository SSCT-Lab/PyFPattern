

def on_open_shell(self):
    try:
        self._exec_cli_command(b'no pag')
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to set terminal parameters')
