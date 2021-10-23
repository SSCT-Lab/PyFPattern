def __init__(self, module, device_ids=None, output_device=None, dim=0):
    super(DataParallel, self).__init__()
    if (not torch.cuda.is_available()):
        self.module = module
        self.device_ids = []
        return
    if (device_ids is None):
        device_ids = list(range(torch.cuda.device_count()))
    if (output_device is None):
        output_device = device_ids[0]
    self.dim = dim
    self.module = module
    self.device_ids = device_ids
    self.output_device = output_device
    if (len(self.device_ids) == 1):
        self.module.cuda(device_ids[0])