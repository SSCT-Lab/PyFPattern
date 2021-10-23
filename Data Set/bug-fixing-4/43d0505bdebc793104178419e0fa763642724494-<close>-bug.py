def close(self):
    display.vvv('closing connection', host=self._play_context.remote_addr)
    self.close_shell()
    super(Connection, self).close()