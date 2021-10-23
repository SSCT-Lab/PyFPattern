

def on_open_shell(self):
    try:
        self._exec_cli_command(b'modify cli preference display-threshold 0 pager disabled')
    except AnsibleConnectionFailure:
        raise AnsibleConnectionFailure('unable to set terminal parameters')
