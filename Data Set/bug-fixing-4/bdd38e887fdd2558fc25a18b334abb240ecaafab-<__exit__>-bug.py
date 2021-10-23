def __exit__(self, typ, value, traceback):
    for c in reversed(self._contexts):
        c.__exit__(typ, value, traceback)