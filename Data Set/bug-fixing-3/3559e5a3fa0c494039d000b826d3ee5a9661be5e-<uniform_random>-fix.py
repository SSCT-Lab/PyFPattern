def uniform_random(shape, dtype='float32', min=(- 1.0), max=1.0, seed=0):
    '\n    This operator initializes a variable with random values sampled from a\n    uniform distribution. The random result is in set [min, max].\n\n    Args:\n        shape (list): The shape of output variable.\n        dtype(np.dtype|core.VarDesc.VarType|str): The type of data, such as\n            float32, float64 etc. Default: float32.\n        min (float): Minimum value of uniform random. Default -1.0.\n        max (float): Maximun value of uniform random. Default 1.0.\n        seed (int): Random seed used for generating samples. 0 means use a\n            seed generated by the system. Note that if seed is not 0, this\n            operator will always generate the same random numbers every time.\n            Default 0.\n\n    Examples:\n        .. code-block:: python\n     \n            import paddle.fluid as fluid\n            result = fluid.layers.uniform_random(shape=[32, 784])\n    '
    if (not isinstance(dtype, core.VarDesc.VarType)):
        dtype = convert_np_dtype_to_dtype_(dtype)
    locals_var = locals().copy()
    kwargs = dict()
    for (name, val) in locals_var.items():
        if (val is not None):
            kwargs[name] = val
    return _uniform_random_(**kwargs)