@add_arg_scope
def fully_connected(inputs, num_outputs, activation_fn=nn.relu, normalizer_fn=None, normalizer_params=None, weights_initializer=initializers.xavier_initializer(), weights_regularizer=None, biases_initializer=init_ops.zeros_initializer(), biases_regularizer=None, reuse=None, variables_collections=None, outputs_collections=None, trainable=True, scope=None):
    'Adds a fully connected layer.\n\n  `fully_connected` creates a variable called `weights`, representing a fully\n  connected weight matrix, which is multiplied by the `inputs` to produce a\n  `Tensor` of hidden units. If a `normalizer_fn` is provided (such as\n  `batch_norm`), it is then applied. Otherwise, if `normalizer_fn` is\n  None and a `biases_initializer` is provided then a `biases` variable would be\n  created and added the hidden units. Finally, if `activation_fn` is not `None`,\n  it is applied to the hidden units as well.\n\n  Note: that if `inputs` have a rank greater than 2, then `inputs` is flattened\n  prior to the initial matrix multiply by `weights`.\n\n  Args:\n    inputs: A tensor of at least rank 2 and static value for the last dimension;\n      i.e. `[batch_size, depth]`, `[None, None, None, channels]`.\n    num_outputs: Integer or long, the number of output units in the layer.\n    activation_fn: Activation function. The default value is a ReLU function.\n      Explicitly set it to None to skip it and maintain a linear activation.\n    normalizer_fn: Normalization function to use instead of `biases`. If\n      `normalizer_fn` is provided then `biases_initializer` and\n      `biases_regularizer` are ignored and `biases` are not created nor added.\n      default set to None for no normalizer function\n    normalizer_params: Normalization function parameters.\n    weights_initializer: An initializer for the weights.\n    weights_regularizer: Optional regularizer for the weights.\n    biases_initializer: An initializer for the biases. If None skip biases.\n    biases_regularizer: Optional regularizer for the biases.\n    reuse: Whether or not the layer and its variables should be reused. To be\n      able to reuse the layer scope must be given.\n    variables_collections: Optional list of collections for all the variables or\n      a dictionary containing a different list of collections per variable.\n    outputs_collections: Collection to add the outputs.\n    trainable: If `True` also add variables to the graph collection\n      `GraphKeys.TRAINABLE_VARIABLES` (see tf.Variable).\n    scope: Optional scope for variable_scope.\n\n  Returns:\n     The tensor variable representing the result of the series of operations.\n\n  Raises:\n    ValueError: If x has rank less than 2 or if its last dimension is not set.\n  '
    if (not isinstance(num_outputs, six.integer_types)):
        raise ValueError('num_outputs should be int or long, got %s.', num_outputs)
    layer_variable_getter = _build_variable_getter({
        'bias': 'biases',
        'kernel': 'weights',
    })
    with variable_scope.variable_scope(scope, 'fully_connected', [inputs], reuse=reuse, custom_getter=layer_variable_getter) as sc:
        inputs = ops.convert_to_tensor(inputs)
        layer = core_layers.Dense(units=num_outputs, activation=None, use_bias=((not normalizer_fn) and biases_initializer), kernel_initializer=weights_initializer, bias_initializer=biases_initializer, kernel_regularizer=weights_regularizer, bias_regularizer=biases_regularizer, activity_regularizer=None, trainable=trainable, name=sc.name, dtype=inputs.dtype.base_dtype, _scope=sc, _reuse=reuse)
        outputs = layer.apply(inputs)
        _add_variable_to_collections(layer.kernel, variables_collections, 'weights')
        if (layer.bias is not None):
            _add_variable_to_collections(layer.bias, variables_collections, 'biases')
        if (normalizer_fn is not None):
            if (not normalizer_params):
                normalizer_params = {
                    
                }
            outputs = normalizer_fn(outputs, **normalizer_params)
        if (activation_fn is not None):
            outputs = activation_fn(outputs)
        return utils.collect_named_outputs(outputs_collections, sc.original_name_scope, outputs)