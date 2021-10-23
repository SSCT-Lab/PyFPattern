def fetch_file(self, in_path, out_path):
    ' Fetch a file from container to local. '
    super(Connection, self).fetch_file(in_path, out_path)
    display.vvv(('FETCH %s TO %s' % (in_path, out_path)), host=self._play_context.remote_addr)
    in_path = self._prefix_login_path(in_path)
    out_dir = os.path.dirname(out_path)
    args = [self.docker_cmd, 'cp', ('%s:%s' % (self._play_context.remote_addr, in_path)), out_dir]
    args = [to_bytes(i, errors='surrogate_or_strict') for i in args]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    actual_out_path = os.path.join(out_dir, os.path.basename(in_path))
    if (p.returncode != 0):
        args = self._build_exec_cmd([self._play_context.executable, '-c', ('dd if=%s bs=%s' % (in_path, BUFSIZE))])
        args = [to_bytes(i, errors='surrogate_or_strict') for i in args]
        with open(to_bytes(actual_out_path, errors='surrogate_or_strict'), 'wb') as out_file:
            try:
                p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=out_file, stderr=subprocess.PIPE)
            except OSError:
                raise AnsibleError('docker connection requires dd command in the container to put files')
            (stdout, stderr) = p.communicate()
            if (p.returncode != 0):
                raise AnsibleError(('failed to fetch file %s to %s:\n%s\n%s' % (in_path, out_path, stdout, stderr)))
    if (actual_out_path != out_path):
        os.rename(to_bytes(actual_out_path, errors='strict'), to_bytes(out_path, errors='strict'))