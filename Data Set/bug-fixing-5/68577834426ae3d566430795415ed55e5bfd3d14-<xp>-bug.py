@property
def xp(self):
    if self.use_chainerx:
        return chainerx
    if self.use_cuda:
        return cuda.cupy
    return numpy