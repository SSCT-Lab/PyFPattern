

@tf_export('random_uniform')
def random_uniform(shape, minval=0, maxval=None, dtype=dtypes.float32, seed=None, name=None):
    'Outputs random values from a uniform distribution.\n\n  The generated values follow a uniform distribution in the range\n  `[minval, maxval)`. The lower bound `minval` is included in the range, while\n  the upper bound `maxval` is excluded.\n\n  For floats, the default range is `[0, 1)`.  For ints, at least `maxval` must\n  be specified explicitly.\n\n  In the integer case, the random integers are slightly biased unless\n  `maxval - minval` is an exact power of two.  The bias is small for values of\n  `maxval - minval` significantly smaller than the range of the output (either\n  `2**32` or `2**64`).\n\n  Args:\n    shape: A 1-D integer Tensor or Python array. The shape of the output tensor.\n    minval: A 0-D Tensor or Python value of type `dtype`. The lower bound on the\n      range of random values to generate.  Defaults to 0.\n    maxval: A 0-D Tensor or Python value of type `dtype`. The upper bound on\n      the range of random values to generate.  Defaults to 1 if `dtype` is\n      floating point.\n    dtype: The type of the output: `float16`, `float32`, `float64`, `int32`,\n      or `int64`.\n    seed: A Python integer. Used to create a random seed for the distribution.\n      See @{tf.set_random_seed}\n      for behavior.\n    name: A name for the operation (optional).\n\n  Returns:\n    A tensor of the specified shape filled with random uniform values.\n\n  Raises:\n    ValueError: If `dtype` is integral and `maxval` is not specified.\n  '
    dtype = dtypes.as_dtype(dtype)
    if (dtype not in (dtypes.float16, dtypes.bfloat16, dtypes.float32, dtypes.float64, dtypes.int32, dtypes.int64)):
        raise ValueError(('Invalid dtype %r' % dtype))
    if (maxval is None):
        if dtype.is_integer:
            raise ValueError(('Must specify maxval for integer dtype %r' % dtype))
        maxval = 1
    with ops.name_scope(name, 'random_uniform', [shape, minval, maxval]) as name:
        shape = _ShapeTensor(shape)
        minval = ops.convert_to_tensor(minval, dtype=dtype, name='min')
        maxval = ops.convert_to_tensor(maxval, dtype=dtype, name='max')
        (seed1, seed2) = random_seed.get_seed(seed)
        if dtype.is_integer:
            return gen_random_ops.random_uniform_int(shape, minval, maxval, seed=seed1, seed2=seed2, name=name)
        else:
            rnd = gen_random_ops.random_uniform(shape, dtype, seed=seed1, seed2=seed2)
            return math_ops.add((rnd * (maxval - minval)), minval, name=name)
