@_ssh_retry
def _run(self, cmd, in_data, sudoable=True, checkrc=True):
    'Wrapper around _bare_run that retries the connection\n        '
    return self._bare_run(cmd, in_data, sudoable=sudoable, checkrc=checkrc)