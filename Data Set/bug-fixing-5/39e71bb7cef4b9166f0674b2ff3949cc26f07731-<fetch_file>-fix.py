def fetch_file(self, in_path, out_path):
    ' fetch a file from local to local -- for compatibility '
    super(Connection, self).fetch_file(in_path, out_path)
    display.vvv('FETCH {0} TO {1}'.format(in_path, out_path), host=self._play_context.remote_addr)
    self.put_file(in_path, out_path)