def put_file(self, in_path, out_path):
    ' put a file from local to lxd '
    super(Connection, self).put_file(in_path, out_path)
    self._display.vvv('PUT {0} TO {1}'.format(in_path, out_path), host=self._host)
    if (not os.path.isfile(to_bytes(in_path, errors='surrogate_or_strict'))):
        raise AnsibleFileNotFound(('input path is not a file: %s' % in_path))
    local_cmd = [self._lxc_cmd, 'file', 'push', in_path, ((self._host + '/') + out_path)]
    local_cmd = [to_bytes(i, errors='surrogate_or_strict') for i in local_cmd]
    call(local_cmd)