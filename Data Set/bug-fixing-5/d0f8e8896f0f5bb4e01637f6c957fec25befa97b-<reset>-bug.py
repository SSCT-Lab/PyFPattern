def reset(self):
    'Reset the connection.'
    super(Connection, self).reset()
    self.close()
    self._connect()