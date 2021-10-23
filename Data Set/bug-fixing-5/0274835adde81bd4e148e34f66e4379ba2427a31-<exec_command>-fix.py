@ensure_connect
def exec_command(self, cmd, in_data=None, sudoable=False):
    ' run specified command in a running OCI container using buildah '
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    cmd_args_list = shlex.split(to_native(cmd, errors='surrogate_or_strict'))
    (rc, stdout, stderr) = self._buildah('run', cmd_args_list)
    display.vvvvv(('STDOUT %r STDERR %r' % (stderr, stderr)))
    return (rc, stdout, stderr)