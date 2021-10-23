def _elementwise_op(helper):
    op_type = helper.layer_type
    x = helper.kwargs.get('x', None)
    y = helper.kwargs.get('y', None)
    if in_dygraph_mode():
        x = base.to_variable(x)
        y = base.to_variable(y)
    assert (x is not None), 'x cannot be None in {}'.format(op_type)
    assert (y is not None), 'y cannot be None in {}'.format(op_type)
    if (not isinstance(x, Variable)):
        raise TypeError(("The type of 'x' in %s must be Variable, but received %s" % (op_type, type(x))))
    if (not isinstance(y, Variable)):
        raise TypeError(("The type of 'y' in %s must be Variable, but received %s" % (op_type, type(y))))
    if (convert_dtype(x.dtype) in ['float16']):
        warnings.warn(("The data type of 'x' in %s only support float16 on GPU now." % op_type))
    if (convert_dtype(y.dtype) in ['float16']):
        warnings.warn(("The data type of 'y' in %s only support float16 on GPU now." % op_type))
    if (convert_dtype(x.dtype) not in ['float16', 'float32', 'float64', 'int32', 'int64']):
        raise TypeError(("The data type of 'x' in %s must be float16 or float32 or float64 or int32 or int64, but received %s." % (op_type, convert_dtype(x.dtype))))
    if (convert_dtype(y.dtype) not in ['float16', 'float32', 'float64', 'int32', 'int64']):
        raise TypeError(("The data type of 'y' in %s must be float16 or float32 or float64 or int32 or int64, but received %s." % (op_type, convert_dtype(y.dtype))))
    axis = helper.kwargs.get('axis', (- 1))
    use_mkldnn = helper.kwargs.get('use_mkldnn', False)
    name = helper.kwargs.get('name', None)
    if (name is None):
        out = helper.create_variable_for_type_inference(dtype=x.dtype)
    else:
        out = helper.create_variable(name=name, dtype=x.dtype, persistable=False)
    helper.append_op(type=op_type, inputs={
        'X': x,
        'Y': y,
    }, outputs={
        'Out': out,
    }, attrs={
        'axis': axis,
        'use_mkldnn': use_mkldnn,
    })
    return helper.append_activation(out)