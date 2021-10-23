def lock_config(self):
    try:
        self.config.lock()
        self._locked = True
    except LockError:
        exc = get_exception()
        raise NetworkError(('unable to lock config: %s' % str(exc)))