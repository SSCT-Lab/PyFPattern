def forward(self, *inputs, **kwargs):
    if (not self.device_ids):
        return self.module(*inputs, **kwargs)
    (inputs, kwargs) = self.scatter(inputs, kwargs, self.device_ids)
    if (len(self.device_ids) == 1):
        return self.module(*inputs[0], **kwargs[0])
    replicas = self.replicate(self.module, self.device_ids[:len(inputs)])
    outputs = self.parallel_apply(replicas, inputs, kwargs)
    return self.gather(outputs, self.output_device)