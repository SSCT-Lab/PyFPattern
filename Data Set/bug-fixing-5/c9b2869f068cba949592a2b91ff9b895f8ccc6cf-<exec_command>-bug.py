def exec_command(self, cmd, in_data=None, sudoable=True):
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    (p, out, err) = self._do_it(('EXEC: ' + cmd))
    return (p.returncode, out, err)