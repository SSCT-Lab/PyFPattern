def fetch_file(self, in_path, out_path):
    ' fetch a file from jail to local '
    super(Connection, self).fetch_file(in_path, out_path)
    display.vvv(('FETCH %s TO %s' % (in_path, out_path)), host=self.jail)
    in_path = shlex_quote(self._prefix_login_path(in_path))
    try:
        p = self._buffered_exec_command(('dd if=%s bs=%s' % (in_path, BUFSIZE)))
    except OSError:
        raise AnsibleError('jail connection requires dd command in the jail')
    with open(to_bytes(out_path, errors='surrogate_or_strict'), 'wb+') as out_file:
        try:
            chunk = p.stdout.read(BUFSIZE)
            while chunk:
                out_file.write(chunk)
                chunk = p.stdout.read(BUFSIZE)
        except:
            traceback.print_exc()
            raise AnsibleError(('failed to transfer file %s to %s' % (in_path, out_path)))
        (stdout, stderr) = p.communicate()
        if (p.returncode != 0):
            raise AnsibleError(('failed to transfer file %s to %s:\n%s\n%s' % (in_path, out_path, to_native(stdout), to_native(stderr))))