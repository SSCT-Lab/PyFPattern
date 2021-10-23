def _assert_input_compatibility(self, inputs):
    'Checks compatibility between the layer and provided inputs.\n\n    This checks that the tensor(s) `inputs` verify the input assumptions\n    of the layer (if any). If not, a clear and actional exception gets raised.\n\n    Arguments:\n        inputs: input tensor or list of input tensors.\n\n    Raises:\n        ValueError: in case of mismatch between\n            the provided inputs and the expectations of the layer.\n    '
    if (not self.input_spec):
        return
    if (not isinstance(self.input_spec, (list, tuple))):
        input_spec = _to_list(self.input_spec)
    else:
        input_spec = self.input_spec
    inputs = _to_list(inputs)
    if (len(inputs) != len(input_spec)):
        raise ValueError(((((((('Layer ' + self.name) + ' expects ') + str(len(input_spec))) + ' inputs, but it received ') + str(len(inputs))) + ' input tensors. Inputs received: ') + str(inputs)))
    for (input_index, (x, spec)) in enumerate(zip(inputs, input_spec)):
        if (spec is None):
            continue
        if ((spec.ndim is not None) or (spec.min_ndim is not None) or (spec.max_ndim is not None)):
            if (x.get_shape().ndims is None):
                raise ValueError((((('Input ' + str(input_index)) + ' of layer ') + self.name) + ' is incompatible with the layer: its rank is undefined, but the layer requires a defined rank.'))
        if (spec.ndim is not None):
            ndim = x.get_shape().ndims
            if (ndim != spec.ndim):
                raise ValueError(((((((((('Input ' + str(input_index)) + ' of layer ') + self.name) + ' is incompatible with the layer: expected ndim=') + str(spec.ndim)) + ', found ndim=') + str(ndim)) + '. Full shape received: ') + str(x.get_shape().as_list())))
        if (spec.max_ndim is not None):
            ndim = x.get_shape().ndims
            if ((ndim is not None) and (ndim > spec.max_ndim)):
                raise ValueError(((((((('Input ' + str(input_index)) + ' of layer ') + self.name) + ' is incompatible with the layer: expected max_ndim=') + str(spec.max_ndim)) + ', found ndim=') + str(ndim)))
        if (spec.min_ndim is not None):
            ndim = x.get_shape().ndims
            if ((ndim is not None) and (ndim < spec.min_ndim)):
                raise ValueError(((((((((('Input ' + str(input_index)) + ' of layer ') + self.name) + ' is incompatible with the layer: : expected min_ndim=') + str(spec.min_ndim)) + ', found ndim=') + str(ndim)) + '. Full shape received: ') + str(x.get_shape().as_list())))
        if (spec.dtype is not None):
            if (x.dtype != spec.dtype):
                raise ValueError(((((((('Input ' + str(input_index)) + ' of layer ') + self.name) + ' is incompatible with the layer: expected dtype=') + str(spec.dtype)) + ', found dtype=') + str(x.dtype)))
        if spec.axes:
            shape = x.get_shape().as_list()
            if (shape is not None):
                for (axis, value) in spec.axes.items():
                    if hasattr(value, 'value'):
                        value = value.value
                    if ((value is not None) and (shape[int(axis)] not in {value, None})):
                        raise ValueError(((((((((('Input ' + str(input_index)) + ' of layer ') + self.name) + ' is incompatible with the layer: expected axis ') + str(axis)) + ' of input shape to have value ') + str(value)) + ' but received input with shape ') + str(shape)))
        if (spec.shape is not None):
            shape = x.get_shape().as_list()
            if (shape is not None):
                for (spec_dim, dim) in zip(spec.shape, shape):
                    if ((spec_dim is not None) and (dim is not None)):
                        if (spec_dim != dim):
                            raise ValueError(((((((('Input ' + str(input_index)) + ' is incompatible with layer ') + self.name) + ': expected shape=') + str(spec.shape)) + ', found shape=') + str(shape)))