def _ConstantValue(tensor, partial):
    if (not isinstance(tensor, ops.Tensor)):
        raise TypeError('tensor is not a Tensor')
    if (tensor.op.type == 'Const'):
        return MakeNdarray(tensor.op.get_attr('value'))
    elif (tensor.op.type == 'Shape'):
        input_shape = tensor.op.inputs[0].get_shape()
        if input_shape.is_fully_defined():
            return np.array([dim.value for dim in input_shape.dims], dtype=tensor.dtype.as_numpy_dtype)
        else:
            return None
    elif (tensor.op.type == 'Size'):
        input_shape = tensor.op.inputs[0].get_shape()
        if input_shape.is_fully_defined():
            return np.prod([dim.value for dim in input_shape.dims], dtype=np.int32)
        else:
            return None
    elif (tensor.op.type == 'Rank'):
        input_shape = tensor.op.inputs[0].get_shape()
        if (input_shape.ndims is not None):
            return np.ndarray(shape=(), buffer=np.array([input_shape.ndims]), dtype=np.int32)
        else:
            return None
    elif (tensor.op.type == 'Range'):
        start = constant_value(tensor.op.inputs[0])
        if (start is None):
            return None
        limit = constant_value(tensor.op.inputs[1])
        if (limit is None):
            return None
        delta = constant_value(tensor.op.inputs[2])
        if (delta is None):
            return None
        return np.arange(start, limit, delta, dtype=tensor.dtype.as_numpy_dtype)
    elif (tensor.op.type == 'Cast'):
        pre_cast = constant_value(tensor.op.inputs[0])
        if (pre_cast is None):
            return None
        cast_dtype = dtypes.as_dtype(tensor.op.get_attr('DstT'))
        return pre_cast.astype(cast_dtype.as_numpy_dtype)
    elif (tensor.op.type == 'Concat'):
        dim = constant_value(tensor.op.inputs[0])
        if (dim is None):
            return None
        values = []
        for x in tensor.op.inputs[1:]:
            value = constant_value(x)
            if (value is None):
                return None
            values.append(value)
        return np.concatenate(values, axis=dim)
    elif (tensor.op.type == 'ConcatV2'):
        dim = constant_value(tensor.op.inputs[(- 1)])
        if (dim is None):
            return None
        values = []
        for x in tensor.op.inputs[:(- 1)]:
            value = constant_value(x)
            if (value is None):
                return None
            values.append(value)
        return np.concatenate(values, axis=dim)
    elif (tensor.op.type == 'Pack'):
        values = []
        if (not tensor.op.inputs):
            return None
        for x in tensor.op.inputs:
            value = constant_value(x, partial)
            if ((value is None) and (not partial)):
                return None
            values.append(value)
        return np.array(values)
    elif (tensor.op.type == 'Fill'):
        fill_shape = tensor.shape
        fill_value = constant_value(tensor.op.inputs[1])
        if (fill_shape.is_fully_defined() and (fill_value is not None)):
            return np.full(fill_shape.as_list(), fill_value, dtype=fill_value.dtype)
        else:
            return None
    elif (tensor.op.type == 'Equal'):
        value1 = constant_value(tensor.op.inputs[0])
        if (value1 is None):
            return None
        value2 = constant_value(tensor.op.inputs[1])
        if (value2 is None):
            return None
        return np.equal(value1, value2)
    elif (tensor.op.type == 'NotEqual'):
        value1 = constant_value(tensor.op.inputs[0])
        if (value1 is None):
            return None
        value2 = constant_value(tensor.op.inputs[1])
        if (value2 is None):
            return None
        return np.not_equal(value1, value2)
    else:
        return None