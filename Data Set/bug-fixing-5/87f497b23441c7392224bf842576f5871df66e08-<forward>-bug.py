def forward(self, inputs):
    self.input_shape = inputs[0].shape
    self.input_dtype = inputs[0].dtype
    xp = backend.get_array_module(*inputs)
    return (xp.empty((0,), dtype=inputs[0].dtype),)