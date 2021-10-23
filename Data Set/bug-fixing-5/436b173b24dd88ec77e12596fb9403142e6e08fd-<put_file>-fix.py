def put_file(self, in_path, out_path):
    ' transfer a file from local to jail '
    super(Connection, self).put_file(in_path, out_path)
    display.vvv(('PUT %s TO %s' % (in_path, out_path)), host=self.jail)
    out_path = shlex_quote(self._prefix_login_path(out_path))
    try:
        with open(to_bytes(in_path, errors='surrogate_or_strict'), 'rb') as in_file:
            try:
                p = self._buffered_exec_command(('dd of=%s bs=%s' % (out_path, BUFSIZE)), stdin=in_file)
            except OSError:
                raise AnsibleError('jail connection requires dd command in the jail')
            try:
                (stdout, stderr) = p.communicate()
            except:
                traceback.print_exc()
                raise AnsibleError(('failed to transfer file %s to %s' % (in_path, out_path)))
            if (p.returncode != 0):
                raise AnsibleError(('failed to transfer file %s to %s:\n%s\n%s' % (in_path, out_path, to_native(stdout), to_native(stderr))))
    except IOError:
        raise AnsibleError(('file or module does not exist at: %s' % in_path))