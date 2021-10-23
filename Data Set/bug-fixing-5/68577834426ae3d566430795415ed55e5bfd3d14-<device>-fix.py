@property
def device(self):
    if (self._device is None):
        if self.use_cuda:
            device = backend.GpuDevice.from_device_id(self.cuda_device)
        elif self.use_chainerx:
            device = backend.ChainerxDevice(chainerx.get_device(self.chainerx_device))
        elif (self.use_ideep != 'never'):
            device = backend.Intel64Device()
        else:
            device = backend.CpuDevice()
        self._device = device
    return self._device