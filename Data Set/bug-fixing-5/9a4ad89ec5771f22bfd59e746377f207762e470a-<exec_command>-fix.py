def exec_command(self, cmd, in_data=None, sudoable=False):
    ' run a command on the chroot '
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    executable = to_native(self._play_context.executable, errors='surrogate_or_strict')
    local_cmd = [executable, '-c', to_native(cmd, errors='surrogate_or_strict')]
    (read_stdout, write_stdout) = (None, None)
    (read_stderr, write_stderr) = (None, None)
    (read_stdin, write_stdin) = (None, None)
    try:
        (read_stdout, write_stdout) = os.pipe()
        (read_stderr, write_stderr) = os.pipe()
        kwargs = {
            'stdout': self._set_nonblocking(write_stdout),
            'stderr': self._set_nonblocking(write_stderr),
            'env_policy': _lxc.LXC_ATTACH_CLEAR_ENV,
        }
        if in_data:
            (read_stdin, write_stdin) = os.pipe()
            kwargs['stdin'] = self._set_nonblocking(read_stdin)
        self._display.vvv(('EXEC %s' % local_cmd), host=self.container_name)
        pid = self.container.attach(_lxc.attach_run_command, local_cmd, **kwargs)
        if (pid == (- 1)):
            msg = ('failed to attach to container %s' % self.container_name)
            raise errors.AnsibleError(msg)
        write_stdout = os.close(write_stdout)
        write_stderr = os.close(write_stderr)
        if read_stdin:
            read_stdin = os.close(read_stdin)
        return self._communicate(pid, in_data, write_stdin, read_stdout, read_stderr)
    finally:
        fds = [read_stdout, write_stdout, read_stderr, write_stderr, read_stdin, write_stdin]
        for fd in fds:
            if fd:
                os.close(fd)