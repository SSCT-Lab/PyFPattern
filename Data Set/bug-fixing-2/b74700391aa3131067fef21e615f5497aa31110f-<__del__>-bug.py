

def __del__(self):
    curand.destroyGenerator(self._generator)
