def cpu_only(inner):

    def outer(self, *args, **kwargs):
        if self.is_cuda:
            raise unittest.SkipTest('Test is CPU-only')
        inner(self, *args, **kwargs)
    return outer