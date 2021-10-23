def exec_command(self, cmd, in_data=None, sudoable=True):
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    return self._do_it(('EXEC: ' + cmd))