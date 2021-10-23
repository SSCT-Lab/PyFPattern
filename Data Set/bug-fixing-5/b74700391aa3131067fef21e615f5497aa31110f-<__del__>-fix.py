def __del__(self):
    if hasattr(self, '_generator'):
        curand.destroyGenerator(self._generator)