

def assert_input_compatibility(self, inputs):
    'Checks compatibility between the layer and provided inputs.\n\n        This checks that the tensor(s) `input`\n        verify the input assumptions of the layer\n        (if any). If not, exceptions are raised.\n\n        # Arguments\n            inputs: input tensor or list of input tensors.\n\n        # Raises\n            ValueError: in case of mismatch between\n                the provided inputs and the expectations of the layer.\n        '
    if (not self.input_spec):
        return
    if (not isinstance(self.input_spec, (list, tuple))):
        input_spec = _to_list(self.input_spec)
    else:
        input_spec = self.input_spec
    inputs = _to_list(inputs)
    if (len(inputs) != len(input_spec)):
        raise ValueError(((((((('Layer ' + self.name) + ' expects ') + str(len(input_spec))) + ' inputs, but it received ') + str(len(inputs))) + ' input tensors. Input received: ') + str(inputs)))
    for (input_index, (x, spec)) in enumerate(zip(inputs, input_spec)):
        if (spec is None):
            continue
        if (spec.ndim is not None):
            if (K.ndim(x) != spec.ndim):
                raise ValueError(((((((('Input ' + str(input_index)) + ' is incompatible with layer ') + self.name) + ': expected ndim=') + str(spec.ndim)) + ', found ndim=') + str(K.ndim(x))))
        if (spec.max_ndim is not None):
            ndim = K.ndim(x)
            if ((ndim is not None) and (ndim > spec.max_ndim)):
                raise ValueError(((((((('Input ' + str(input_index)) + ' is incompatible with layer ') + self.name) + ': expected max_ndim=') + str(spec.max_ndim)) + ', found ndim=') + str(K.ndim(x))))
        if (spec.min_ndim is not None):
            ndim = K.ndim(x)
            if ((ndim is not None) and (ndim < spec.min_ndim)):
                raise ValueError(((((((('Input ' + str(input_index)) + ' is incompatible with layer ') + self.name) + ': expected min_ndim=') + str(spec.min_ndim)) + ', found ndim=') + str(K.ndim(x))))
        if (spec.dtype is not None):
            if (K.dtype(x) != spec.dtype):
                raise ValueError(((((((('Input ' + str(input_index)) + ' is incompatible with layer ') + self.name) + ': expected dtype=') + str(spec.dtype)) + ', found dtype=') + str(K.dtype(x))))
        if spec.axes:
            try:
                x_shape = K.int_shape(x)
            except TypeError:
                x_shape = None
            if (x_shape is not None):
                for (axis, value) in spec.axes.items():
                    if ((value is not None) and (x_shape[int(axis)] not in {value, None})):
                        raise ValueError(((((((((('Input ' + str(input_index)) + ' is incompatible with layer ') + self.name) + ': expected axis ') + str(axis)) + ' of input shape to have value ') + str(value)) + ' but got shape ') + str(x_shape)))
        if (spec.shape is not None):
            try:
                x_shape = K.int_shape(x)
            except TypeError:
                x_shape = None
            if (x_shape is not None):
                for (spec_dim, dim) in zip(spec.shape, x_shape):
                    if ((spec_dim is not None) and (dim is not None)):
                        if (spec_dim != dim):
                            raise ValueError(((((((('Input ' + str(input_index)) + ' is incompatible with layer ') + self.name) + ': expected shape=') + str(spec.shape)) + ', found shape=') + str(x_shape)))
