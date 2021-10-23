def increment(x, value=1.0, in_place=True):
    "\n    This function performs an operation that increments the value in the\n    input :math:`x` by an amount: :math:`value` as mentioned in the input\n    parameter. This operation is performed in-place by default. Notice that\n    the number of elements in :math:`x` must be equal to 1.\n\n    Args:\n        x (Variable|list): The tensor that has the input values.\n        value (float): The amount by which the values should be incremented.\n        in_place (bool): If the increment should be performed in-place.\n\n    Returns:\n        Variable: The elementwise-incremented object.\n\n    Examples:\n        .. code-block:: python\n\n          data = fluid.layers.data(name='data', shape=[1], dtype='float32',\n                                   append_batch_size=False)\n          data = fluid.layers.increment(x=data, value=3.0, in_place=True)\n    "
    helper = LayerHelper('increment', **locals())
    if (not in_place):
        out = helper.create_variable_for_type_inference(dtype=x.dtype)
    else:
        out = x
    helper.append_op(type='increment', inputs={
        'X': [x],
    }, outputs={
        'Out': [out],
    }, attrs={
        'step': float(value),
    })
    return out