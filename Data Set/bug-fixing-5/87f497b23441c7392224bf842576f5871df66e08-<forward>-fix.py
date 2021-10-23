def forward(self, inputs):
    xp = backend.get_array_module(inputs[0])
    return (xp.empty((0,), dtype=numpy.float32),)