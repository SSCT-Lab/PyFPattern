@templatedoc()
def sequence_pad(x, pad_value, maxlen=None, name=None):
    "\n    ${comment}\n\n    Args:\n        x(Variable): Input variable which should contain lod information.\n        pad_value(Variable): The Variable that holds values that will be fill\n            into padded steps. It can be a scalar or a tensor whose shape\n            equals to time steps in sequences. If it's a scalar, it will be\n            automatically broadcasted to the shape of time step.\n        maxlen(int, default None): The length of padded sequences. It can be\n            None or any positive int. When it is None, all sequences will be\n            padded up to the length of the longest one among them; when it a\n            certain positive value, it must be greater than the length of the\n            longest original sequence.\n        name(str|None): A name for this layer(optional). If set None, the layer\n            will be named automatically.\n\n    Returns:\n        Variable: The padded sequence batch and the original lengths before\n                  padding. All sequences has the same length.\n\n    Examples:\n        .. code-block:: python\n\n            import numpy\n\n            x = fluid.layers.data(name='y', shape=[10, 5],\n                             dtype='float32', lod_level=1)\n            pad_value = fluid.layers.assign(input=numpy.array([0]))\n            out = fluid.layers.sequence_pad(x=x, pad_value=pad_value)\n    "
    helper = LayerHelper('sequence_pad', input=x, **locals())
    dtype = helper.input_dtype()
    out = helper.create_variable_for_type_inference(dtype)
    length = helper.create_variable_for_type_inference(dtype)
    pad_value.stop_gradient = True
    length.stop_gradient = True
    if (maxlen is None):
        maxlen = (- 1)
    helper.append_op(type='sequence_pad', inputs={
        'X': x,
        'PadValue': pad_value,
    }, outputs={
        'Out': out,
        'Length': length,
    }, attrs={
        'padded_length': maxlen,
    })
    return (out, length)