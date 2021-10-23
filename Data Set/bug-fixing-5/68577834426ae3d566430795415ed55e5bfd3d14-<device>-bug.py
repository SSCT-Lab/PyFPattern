@property
def device(self):
    if (self._device is None):
        if self.use_cuda:
            device = chainer.get_device(chainer.backends.cuda.Device(self.cuda_device))
        elif self.use_chainerx:
            device = chainer.get_device(self.chainerx_device)
        elif (self.use_ideep != 'never'):
            device = backend.Intel64Device()
        else:
            device = backend.CpuDevice()
        self._device = device
    return self._device