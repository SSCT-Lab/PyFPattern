def cpu_only(inner):

    def outer(self, *args, **kwargs):
        unittest.skipIf(self.is_cuda, 'Test is CPU-only')(inner)(self, *args, **kwargs)
    return outer