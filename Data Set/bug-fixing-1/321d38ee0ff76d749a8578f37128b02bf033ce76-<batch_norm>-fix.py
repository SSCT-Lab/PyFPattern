

@add_arg_scope
def batch_norm(inputs, decay=0.999, center=True, scale=False, epsilon=0.001, activation_fn=None, param_initializers=None, updates_collections=ops.GraphKeys.UPDATE_OPS, is_training=True, reuse=None, variables_collections=None, outputs_collections=None, trainable=True, batch_weights=None, fused=False, data_format=DATA_FORMAT_NHWC, zero_debias_moving_mean=False, scope=None):
    'Adds a Batch Normalization layer from http://arxiv.org/abs/1502.03167.\n\n    "Batch Normalization: Accelerating Deep Network Training by Reducing\n    Internal Covariate Shift"\n\n    Sergey Ioffe, Christian Szegedy\n\n  Can be used as a normalizer function for conv2d and fully_connected.\n\n  Note: When is_training is True the moving_mean and moving_variance need to be\n  updated, by default the update_ops are placed in `tf.GraphKeys.UPDATE_OPS` so\n  they need to be added as a dependency to the `train_op`, example:\n\n    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)\n    if update_ops:\n      updates = tf.group(*update_ops)\n      total_loss = control_flow_ops.with_dependencies([updates], total_loss)\n\n  One can set updates_collections=None to force the updates in place, but that\n  can have speed penalty, especially in distributed settings.\n\n  Args:\n    inputs: A tensor with 2 or more dimensions, where the first dimension has\n      `batch_size`. The normalization is over all but the last dimension if\n      `data_format` is `NHWC` and the second dimension if `data_format` is\n      `NCHW`.\n    decay: Decay for the moving average. Reasonable values for `decay` are close\n      to 1.0, typically in the multiple-nines range: 0.999, 0.99, 0.9, etc.\n      Lower `decay` value (recommend trying `decay`=0.9) if model experiences\n      reasonably good training performance but poor validation and/or test\n      performance. Try zero_debias_moving_mean=True for improved stability.\n    center: If True, add offset of `beta` to normalized tensor. If False, `beta`\n      is ignored.\n    scale: If True, multiply by `gamma`. If False, `gamma` is\n      not used. When the next layer is linear (also e.g. `nn.relu`), this can be\n      disabled since the scaling can be done by the next layer.\n    epsilon: Small float added to variance to avoid dividing by zero.\n    activation_fn: Activation function, default set to None to skip it and\n      maintain a linear activation.\n    param_initializers: Optional initializers for beta, gamma, moving mean and\n      moving variance.\n    updates_collections: Collections to collect the update ops for computation.\n      The updates_ops need to be executed with the train_op.\n      If None, a control dependency would be added to make sure the updates are\n      computed in place.\n    is_training: Whether or not the layer is in training mode. In training mode\n      it would accumulate the statistics of the moments into `moving_mean` and\n      `moving_variance` using an exponential moving average with the given\n      `decay`. When it is not in training mode then it would use the values of\n      the `moving_mean` and the `moving_variance`.\n    reuse: Whether or not the layer and its variables should be reused. To be\n      able to reuse the layer scope must be given.\n    variables_collections: Optional collections for the variables.\n    outputs_collections: Collections to add the outputs.\n    trainable: If `True` also add variables to the graph collection\n      `GraphKeys.TRAINABLE_VARIABLES` (see `tf.Variable`).\n    batch_weights: An optional tensor of shape `[batch_size]`,\n      containing a frequency weight for each batch item. If present,\n      then the batch normalization uses weighted mean and\n      variance. (This can be used to correct for bias in training\n      example selection.)\n    fused:  Use nn.fused_batch_norm if True, nn.batch_normalization otherwise.\n    data_format: A string. `NHWC` (default) and `NCHW` are supported.\n    zero_debias_moving_mean: Use zero_debias for moving_mean. It creates a new\n      pair of variables \'moving_mean/biased\' and \'moving_mean/local_step\'.\n    scope: Optional scope for `variable_scope`.\n\n  Returns:\n    A `Tensor` representing the output of the operation.\n\n  Raises:\n    ValueError: If `batch_weights` is not None and `fused` is True.\n    ValueError: If `data_format` is neither `NHWC` nor `NCHW`.\n    ValueError: If the rank of `inputs` is undefined.\n    ValueError: If rank or channels dimension of `inputs` is undefined.\n  '
    if fused:
        if (batch_weights is not None):
            raise ValueError('Weighted mean and variance is not currently supported for fused batch norm.')
        return _fused_batch_norm(inputs, decay=decay, center=center, scale=scale, epsilon=epsilon, activation_fn=activation_fn, param_initializers=param_initializers, updates_collections=updates_collections, is_training=is_training, reuse=reuse, variables_collections=variables_collections, outputs_collections=outputs_collections, trainable=trainable, data_format=data_format, zero_debias_moving_mean=zero_debias_moving_mean, scope=scope)
    if (data_format not in (DATA_FORMAT_NCHW, DATA_FORMAT_NHWC)):
        raise ValueError('data_format has to be either NCHW or NHWC.')
    layer_variable_getter = _build_variable_getter()
    with variable_scope.variable_scope(scope, 'BatchNorm', [inputs], reuse=reuse, custom_getter=layer_variable_getter) as sc:
        inputs = ops.convert_to_tensor(inputs)
        if ((batch_weights is None) and (updates_collections is ops.GraphKeys.UPDATE_OPS) and (not zero_debias_moving_mean)):
            axis = (1 if (data_format == DATA_FORMAT_NCHW) else (- 1))
            if (not param_initializers):
                param_initializers = {
                    
                }
            beta_initializer = param_initializers.get('beta', init_ops.zeros_initializer())
            gamma_initializer = param_initializers.get('gamma', init_ops.ones_initializer())
            moving_mean_initializer = param_initializers.get('moving_mean', init_ops.zeros_initializer())
            moving_variance_initializer = param_initializers.get('moving_variance', init_ops.ones_initializer())
            layer = normalization_layers.BatchNormalization(axis=axis, momentum=decay, epsilon=epsilon, center=center, scale=scale, beta_initializer=beta_initializer, gamma_initializer=gamma_initializer, moving_mean_initializer=moving_mean_initializer, moving_variance_initializer=moving_variance_initializer, trainable=trainable, name=sc.name, _scope=sc, _reuse=reuse)
            outputs = layer.apply(inputs, training=is_training)
            _add_variable_to_collections(layer.moving_mean, variables_collections, 'moving_mean')
            _add_variable_to_collections(layer.moving_variance, variables_collections, 'moving_variance')
            if layer.beta:
                _add_variable_to_collections(layer.beta, variables_collections, 'beta')
            if layer.gamma:
                _add_variable_to_collections(layer.gamma, variables_collections, 'gamma')
            if (activation_fn is not None):
                outputs = activation_fn(outputs)
            return utils.collect_named_outputs(outputs_collections, sc.original_name_scope, outputs)
        inputs_shape = inputs.get_shape()
        inputs_rank = inputs_shape.ndims
        if (inputs_rank is None):
            raise ValueError(('Inputs %s has undefined rank.' % inputs.name))
        dtype = inputs.dtype.base_dtype
        if (batch_weights is not None):
            batch_weights = ops.convert_to_tensor(batch_weights)
            inputs_shape[0:1].assert_is_compatible_with(batch_weights.get_shape())
            nshape = ([(- 1)] + [1 for _ in range((inputs_rank - 1))])
            batch_weights = array_ops.reshape(batch_weights, nshape)
        if (data_format == DATA_FORMAT_NCHW):
            moments_axes = ([0] + list(range(2, inputs_rank)))
            params_shape = inputs_shape[1:2]
            params_shape_broadcast = list(([1, inputs_shape[1].value] + [1 for _ in range(2, inputs_rank)]))
        else:
            moments_axes = list(range((inputs_rank - 1)))
            params_shape = inputs_shape[(- 1):]
            params_shape_broadcast = None
        if (not params_shape.is_fully_defined()):
            raise ValueError(('Inputs %s has undefined channels dimension %s.' % (inputs.name, params_shape)))
        (beta, gamma) = (None, None)
        if (not param_initializers):
            param_initializers = {
                
            }
        if center:
            beta_collections = utils.get_variable_collections(variables_collections, 'beta')
            beta_initializer = param_initializers.get('beta', init_ops.zeros_initializer())
            beta = variables.model_variable('beta', shape=params_shape, dtype=dtype, initializer=beta_initializer, collections=beta_collections, trainable=trainable)
        if scale:
            gamma_collections = utils.get_variable_collections(variables_collections, 'gamma')
            gamma_initializer = param_initializers.get('gamma', init_ops.ones_initializer())
            gamma = variables.model_variable('gamma', shape=params_shape, dtype=dtype, initializer=gamma_initializer, collections=gamma_collections, trainable=trainable)
        partitioner = variable_scope.get_variable_scope().partitioner
        try:
            variable_scope.get_variable_scope().set_partitioner(None)
            moving_mean_collections = utils.get_variable_collections(variables_collections, 'moving_mean')
            moving_mean_initializer = param_initializers.get('moving_mean', init_ops.zeros_initializer())
            moving_mean = variables.model_variable('moving_mean', shape=params_shape, dtype=dtype, initializer=moving_mean_initializer, trainable=False, collections=moving_mean_collections)
            moving_variance_collections = utils.get_variable_collections(variables_collections, 'moving_variance')
            moving_variance_initializer = param_initializers.get('moving_variance', init_ops.ones_initializer())
            moving_variance = variables.model_variable('moving_variance', shape=params_shape, dtype=dtype, initializer=moving_variance_initializer, trainable=False, collections=moving_variance_collections)
        finally:
            variable_scope.get_variable_scope().set_partitioner(partitioner)
        is_training_value = utils.constant_value(is_training)
        need_moments = ((is_training_value is None) or is_training_value)
        if need_moments:
            if (batch_weights is None):
                if (data_format == DATA_FORMAT_NCHW):
                    (mean, variance) = nn.moments(inputs, moments_axes, keep_dims=True)
                    mean = array_ops.reshape(mean, [(- 1)])
                    variance = array_ops.reshape(variance, [(- 1)])
                else:
                    (mean, variance) = nn.moments(inputs, moments_axes)
            elif (data_format == DATA_FORMAT_NCHW):
                (mean, variance) = nn.weighted_moments(inputs, moments_axes, batch_weights, keep_dims=True)
                mean = array_ops.reshape(mean, [(- 1)])
                variance = array_ops.reshape(variance, [(- 1)])
            else:
                (mean, variance) = nn.weighted_moments(inputs, moments_axes, batch_weights)
            moving_vars_fn = (lambda : (moving_mean, moving_variance))
            if (updates_collections is None):

                def _force_updates():
                    'Internal function forces updates moving_vars if is_training.'
                    update_moving_mean = moving_averages.assign_moving_average(moving_mean, mean, decay, zero_debias=zero_debias_moving_mean)
                    update_moving_variance = moving_averages.assign_moving_average(moving_variance, variance, decay, zero_debias=False)
                    with ops.control_dependencies([update_moving_mean, update_moving_variance]):
                        return (array_ops.identity(mean), array_ops.identity(variance))
                (mean, variance) = utils.smart_cond(is_training, _force_updates, moving_vars_fn)
            else:

                def _delay_updates():
                    'Internal function that delay updates moving_vars if is_training.'
                    update_moving_mean = moving_averages.assign_moving_average(moving_mean, mean, decay, zero_debias=zero_debias_moving_mean)
                    update_moving_variance = moving_averages.assign_moving_average(moving_variance, variance, decay, zero_debias=False)
                    return (update_moving_mean, update_moving_variance)
                (update_mean, update_variance) = utils.smart_cond(is_training, _delay_updates, moving_vars_fn)
                ops.add_to_collections(updates_collections, update_mean)
                ops.add_to_collections(updates_collections, update_variance)
                vars_fn = (lambda : (mean, variance))
                (mean, variance) = utils.smart_cond(is_training, vars_fn, moving_vars_fn)
        else:
            (mean, variance) = (moving_mean, moving_variance)
        if (data_format == DATA_FORMAT_NCHW):
            mean = array_ops.reshape(mean, params_shape_broadcast)
            variance = array_ops.reshape(variance, params_shape_broadcast)
            beta = array_ops.reshape(beta, params_shape_broadcast)
            if (gamma is not None):
                gamma = array_ops.reshape(gamma, params_shape_broadcast)
        outputs = nn.batch_normalization(inputs, mean, variance, beta, gamma, epsilon)
        outputs.set_shape(inputs_shape)
        if (activation_fn is not None):
            outputs = activation_fn(outputs)
        return utils.collect_named_outputs(outputs_collections, sc.original_name_scope, outputs)
