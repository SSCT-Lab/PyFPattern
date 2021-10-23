@contextmanager
def lock_file(self, path, lock_timeout=None):
    '\n        Context for lock acquisition\n        '
    try:
        self.set_lock(path, lock_timeout)
        (yield)
    finally:
        self.unlock()