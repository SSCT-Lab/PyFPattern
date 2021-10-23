def _connect(self):
    ' connect to the chroot; nothing to do here '
    super(Connection, self)._connect()
    if (not self._connected):
        display.vvv('THIS IS A LOCAL CHROOT DIR', host=self.chroot)
        self._connected = True