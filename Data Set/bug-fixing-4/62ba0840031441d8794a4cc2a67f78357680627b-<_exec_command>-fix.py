def _exec_command(self, cmd, in_data=None, sudoable=True):
    ' run a command on the remote host '
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    display.vvv('ESTABLISH SSH CONNECTION FOR USER: {0}'.format(self._play_context.remote_user), host=self._play_context.remote_addr)
    if ((not in_data) and sudoable):
        args = ('ssh', '-tt', self.host, cmd)
    else:
        args = ('ssh', self.host, cmd)
    cmd = self._build_command(*args)
    (returncode, stdout, stderr) = self._run(cmd, in_data, sudoable=sudoable)
    return (returncode, stdout, stderr)