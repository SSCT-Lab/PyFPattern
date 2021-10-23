def __exit__(self, typ, value, traceback):
    contexts = self._contexts.pop()
    for c in reversed(contexts):
        c.__exit__(typ, value, traceback)