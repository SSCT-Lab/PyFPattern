

def forward(self, *inputs, **kwargs):
    self.need_reduction = True
    (inputs, kwargs) = self.scatter(inputs, kwargs, self.device_ids)
    self._sync_params()
    if (len(self.device_ids) == 1):
        return self.module(*inputs[0], **kwargs[0])
    outputs = self.parallel_apply(self._module_copies, inputs, kwargs)
    return self.gather(outputs, self.output_device)
