def put_file(self, in_path, out_path):
    ' Transfer a file from local to docker container '
    super(Connection, self).put_file(in_path, out_path)
    display.vvv(('PUT %s TO %s' % (in_path, out_path)), host=self._play_context.remote_addr)
    out_path = self._prefix_login_path(out_path)
    if (not os.path.exists(to_bytes(in_path, errors='surrogate_or_strict'))):
        raise AnsibleFileNotFound(('file or module does not exist: %s' % to_native(in_path)))
    out_path = shlex_quote(out_path)
    args = self._build_exec_cmd([self._play_context.executable, '-c', ('dd of=%s bs=%s' % (out_path, BUFSIZE))])
    args = [to_bytes(i, errors='surrogate_or_strict') for i in args]
    with open(to_bytes(in_path, errors='surrogate_or_strict'), 'rb') as in_file:
        try:
            p = subprocess.Popen(args, stdin=in_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            raise AnsibleError('docker connection requires dd command in the container to put files')
        (stdout, stderr) = p.communicate()
        if (p.returncode != 0):
            raise AnsibleError(('failed to transfer file %s to %s:\n%s\n%s' % (to_native(in_path), to_native(out_path), to_native(stdout), to_native(stderr))))