

def piecewise_constant(x, boundaries, values, name=None):
    "Piecewise constant from boundaries and interval values.\n\n  Example: use a learning rate that's 1.0 for the first 100000 steps, 0.5\n    for steps 100001 to 110000, and 0.1 for any additional steps.\n\n  ```python\n  global_step = tf.Variable(0, trainable=False)\n  boundaries = [100000, 110000]\n  values = [1.0, 0.5, 0.1]\n  learning_rate = tf.train.piecewise_constant(global_step, boundaries, values)\n\n  # Later, whenever we perform an optimization step, we increment global_step.\n  ```\n\n  Args:\n    x: A 0-D scalar `Tensor`. Must be one of the following types: `float32`,\n      `float64`, `uint8`, `int8`, `int16`, `int32`, `int64`.\n    boundaries: A list of `Tensor`s or `int`s or `float`s with strictly\n      increasing entries, and with all elements having the same type as `x`.\n    values: A list of `Tensor`s or float`s or `int`s that specifies the values\n      for the intervals defined by `boundaries`. It should have one more element\n      than `boundaries`, and all elements should have the same type.\n    name: A string. Optional name of the operation. Defaults to\n      'PiecewiseConstant'.\n\n  Returns:\n    A 0-D Tensor. Its value is `values[0]` when `x <= boundaries[0]`,\n    `values[1]` when `x > boundaries[0]` and `x <= boundaries[1]`, ...,\n    and values[-1] when `x > boundaries[-1]`.\n\n  Raises:\n    ValueError: if types of `x` and `boundaries` do not match, or types of all\n        `values` do not match or\n        the number of elements in the lists does not match.\n  "
    if (len(boundaries) != (len(values) - 1)):
        raise ValueError('The length of boundaries should be 1 less than the length of values')
    with ops.name_scope(name, 'PiecewiseConstant', [x, boundaries, values, name]) as name:
        x = ops.convert_to_tensor(x)
        boundaries = ops.convert_n_to_tensor(boundaries)
        for (i, b) in enumerate(boundaries):
            if (b.dtype.base_dtype != x.dtype.base_dtype):
                if ((b.dtype.base_dtype == dtypes.int32) and (x.dtype.base_dtype == dtypes.int64)):
                    b = math_ops.cast(b, x.dtype.base_dtype)
                    boundaries[i] = b
                else:
                    raise ValueError(('Boundaries (%s) must have the same dtype as x (%s).' % (b.dtype.base_dtype, x.dtype.base_dtype)))
        values = ops.convert_n_to_tensor(values)
        for v in values[1:]:
            if (v.dtype.base_dtype != values[0].dtype.base_dtype):
                raise ValueError(('Values must have elements all with the same dtype (%s vs %s).' % (values[0].dtype.base_dtype, v.dtype.base_dtype)))
        pred_fn_pairs = []
        pred_fn_pairs.append(((x <= boundaries[0]), (lambda : values[0])))
        pred_fn_pairs.append(((x > boundaries[(- 1)]), (lambda : values[(- 1)])))
        for (low, high, v) in zip(boundaries[:(- 1)], boundaries[1:], values[1:(- 1)]):
            pred = ((x > low) & (x <= high))
            pred_fn_pairs.append((pred, (lambda v=v: v)))
        default = (lambda : values[0])
        return control_flow_ops.case(pred_fn_pairs, default, exclusive=True)
