def _get_single_variable(self, name, shape=None, dtype=dtypes.float32, initializer=None, regularizer=None, partition_info=None, reuse=None, trainable=True, collections=None, caching_device=None, validate_shape=True, use_resource=None):
    'Get or create a single Variable (e.g. a shard or entire variable).\n\n    See the documentation of get_variable above (ignore partitioning components)\n    for details.\n\n    Args:\n      name: see get_variable.\n      shape: see get_variable.\n      dtype: see get_variable.\n      initializer: see get_variable.\n      regularizer: see get_variable.\n      partition_info: _PartitionInfo object.\n      reuse: see get_variable.\n      trainable: see get_variable.\n      collections: see get_variable.\n      caching_device: see get_variable.\n      validate_shape: see get_variable.\n      use_resource: see get_variable.\n\n    Returns:\n      A Variable.  See documentation of get_variable above.\n\n    Raises:\n      ValueError: See documentation of get_variable above.\n    '
    initializing_from_value = False
    if ((initializer is not None) and (not callable(initializer))):
        initializing_from_value = True
    if ((shape is not None) and initializing_from_value):
        raise ValueError('If initializer is a constant, do not specify shape.')
    should_check = (reuse is not None)
    dtype = dtypes.as_dtype(dtype)
    shape = tensor_shape.as_shape(shape)
    if (name in self._vars):
        if (should_check and (not reuse)):
            tb = self._vars[name].op.traceback[::(- 1)]
            tb = [x for x in tb if ('tensorflow/python' not in x[0])][:3]
            raise ValueError(('Variable %s already exists, disallowed. Did you mean to set reuse=True in VarScope? Originally defined at:\n\n%s' % (name, ''.join(traceback.format_list(tb)))))
        found_var = self._vars[name]
        if (not shape.is_compatible_with(found_var.get_shape())):
            raise ValueError(('Trying to share variable %s, but specified shape %s and found shape %s.' % (name, shape, found_var.get_shape())))
        if (not dtype.is_compatible_with(found_var.dtype)):
            dtype_str = dtype.name
            found_type_str = found_var.dtype.name
            raise ValueError(('Trying to share variable %s, but specified dtype %s and found dtype %s.' % (name, dtype_str, found_type_str)))
        return found_var
    if (should_check and reuse):
        raise ValueError(('Variable %s does not exist, or was not created with tf.get_variable(). Did you mean to set reuse=None in VarScope?' % name))
    if ((not shape.is_fully_defined()) and (not initializing_from_value)):
        raise ValueError(('Shape of a new variable (%s) must be fully defined, but instead was %s.' % (name, shape)))
    if (initializer is None):
        (initializer, initializing_from_value) = self._get_default_initializer(name=name, shape=shape, dtype=dtype)
    with ops.control_dependencies(None):
        if initializing_from_value:
            init_val = initializer
            variable_dtype = None
        else:
            init_val = (lambda : initializer(shape.as_list(), dtype=dtype, partition_info=partition_info))
            variable_dtype = dtype.base_dtype
    if (use_resource is None):
        use_resource = False
    if use_resource:
        v = resource_variable_ops.ResourceVariable(initial_value=init_val, name=name, trainable=trainable, collections=collections, caching_device=caching_device, dtype=variable_dtype, validate_shape=validate_shape)
    else:
        v = variables.Variable(initial_value=init_val, name=name, trainable=trainable, collections=collections, caching_device=caching_device, dtype=variable_dtype, validate_shape=validate_shape)
    self._vars[name] = v
    logging.vlog(1, 'Created variable %s with shape %s and init %s', v.name, format(shape), initializer)
    if regularizer:
        with ops.colocate_with(v.op):
            with ops.name_scope((name + '/Regularizer/')):
                loss = regularizer(v)
            if (loss is not None):
                logging.vlog(1, 'Applied regularizer to %s and added the result %s to REGULARIZATION_LOSSES.', v.name, loss.name)
                ops.add_to_collection(ops.GraphKeys.REGULARIZATION_LOSSES, loss)
    return v