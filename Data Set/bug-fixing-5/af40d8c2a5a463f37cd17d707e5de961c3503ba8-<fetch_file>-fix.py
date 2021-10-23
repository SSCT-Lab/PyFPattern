def fetch_file(self, in_path, out_path):
    ' fetch a file from lxd to local '
    super(Connection, self).fetch_file(in_path, out_path)
    self._display.vvv('FETCH {0} TO {1}'.format(in_path, out_path), host=self._host)
    local_cmd = [self._lxc_cmd, 'file', 'pull', ((self._host + '/') + in_path), out_path]
    local_cmd = [to_bytes(i, errors='surrogate_or_strict') for i in local_cmd]
    process = Popen(local_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process.communicate()