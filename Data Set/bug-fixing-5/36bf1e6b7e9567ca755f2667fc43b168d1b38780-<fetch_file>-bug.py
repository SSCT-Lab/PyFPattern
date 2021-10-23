def fetch_file(self, in_path, out_path):
    ' fetch a file from remote to local '
    in_path = self._normalize_path(in_path, '/')
    vvv(('FETCH %s TO %s' % (in_path, out_path)), host=self.host)
    tmpdir = tempfile.mkdtemp(prefix='func_ansible')
    self.client.local.getfile.get(in_path, tmpdir)
    shutil.move(os.path.join(tmpdir, self.host, os.path.basename(in_path)), out_path)
    shutil.rmtree(tmpdir)