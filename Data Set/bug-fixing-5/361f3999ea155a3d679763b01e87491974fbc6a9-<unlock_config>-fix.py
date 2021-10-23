def unlock_config(self):
    try:
        self.config.unlock()
        self._locked = False
    except UnlockError:
        exc = get_exception()
        raise NetworkError(('unable to unlock config: %s' % str(exc)))