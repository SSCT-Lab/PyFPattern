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
    if (actual_out_path != out_path):
        os.rename(to_bytes(actual_out_path, errors='strict'), to_bytes(out_path, errors='strict'))