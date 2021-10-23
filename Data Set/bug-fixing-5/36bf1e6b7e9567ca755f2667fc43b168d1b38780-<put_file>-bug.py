def put_file(self, in_path, out_path):
    ' transfer a file from local to remote '
    out_path = self._normalize_path(out_path, '/')
    vvv(('PUT %s TO %s' % (in_path, out_path)), host=self.host)
    self.client.local.copyfile.send(in_path, out_path)