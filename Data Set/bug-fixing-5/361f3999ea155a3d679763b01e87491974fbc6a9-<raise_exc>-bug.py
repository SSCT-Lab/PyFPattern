def raise_exc(self, msg):
    if self.device:
        if self._locked:
            self.config.unlock()
        self.disconnect()
    raise NetworkError(msg)