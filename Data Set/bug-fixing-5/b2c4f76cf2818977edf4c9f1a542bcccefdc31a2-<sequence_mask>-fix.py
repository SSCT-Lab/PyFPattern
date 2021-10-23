def sequence_mask(x, maxlen=None, dtype='int64', name=None):
    "\n    **SequenceMask Layer**\n\n    This layer outputs a mask according to the input :code:`x` and\n    :code:`maxlen` with data type of :code:`dtype`.\n\n    Supposing :code:`x` is a Tensor with shape [d_1, d_2, ..., d_n], the\n    :code:`y` is a mask with shape [d_1, d_2, ..., d_n, maxlen], where:\n\n    .. math::\n\n        y(i_1, i_2,..., i_n, j) = (j < x(i_1, i_2,..., i_n))\n\n    Args:\n        x (Variable): Input tensor of sequence_mask layer,\n                      whose elements are integers less than :code:`maxlen`.\n        maxlen (int|None): Maximum length of the sequence. If :code:`maxlen`\n                           is None, it would be replace with :math:`max(x)`.\n        dtype (np.dtype|core.VarDesc.VarType|str): Data type of the output.\n        name (str|None): A name for this layer(optional). If set None, the\n                         layer will be named automatically.\n\n    Returns:\n        Variable: The output sequence mask.\n\n    Examples:\n        .. code-block:: python\n\t\n            import paddle.fluid as fluid\n            import paddle.fluid.layers as layers\n\n            x = fluid.layers.data(name='x', shape=[10], dtype='float32', lod_level=1)\n            mask = layers.sequence_mask(x=x)\n\n    "
    helper = LayerHelper('sequence_mask', **locals())
    if (name is None):
        out = helper.create_variable_for_type_inference(dtype=dtype)
    else:
        out = helper.create_variable_for_type_inference(dtype=dtype, name=name)
    inputs = {
        'X': [x],
    }
    attrs = {
        'out_dtype': out.dtype,
    }
    if (maxlen is not None):
        if isinstance(maxlen, Variable):
            inputs['MaxLenTensor'] = maxlen
        else:
            attrs['maxlen'] = maxlen
    helper.append_op(type='sequence_mask', inputs=inputs, outputs={
        'Y': out,
    }, attrs=attrs)
    out.stop_gradient = True
    return out