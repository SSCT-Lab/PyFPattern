def forward(self, *inputs, **kwargs):
    if (len(self.device_ids) == 1):
        return self.module(*inputs, **kwargs)
    (inputs, kwargs) = self.scatter(inputs, kwargs, self.device_ids)
    self._sync_params()
    outputs = self.parallel_apply(self._module_copies, inputs, kwargs)
    return self.gather(outputs, self.output_device)