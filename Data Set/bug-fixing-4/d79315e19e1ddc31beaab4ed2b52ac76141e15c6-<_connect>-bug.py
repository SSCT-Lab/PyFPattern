def _connect(self):
    super(Connection, self)._connect()
    if (not self.protocol):
        self.protocol = self._winrm_connect()
        self._connected = True
    return self