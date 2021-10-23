def batch_norm(input, act=None, is_test=False, momentum=0.9, epsilon=1e-05, param_attr=None, bias_attr=None, data_layout='NCHW', in_place=False, name=None, moving_mean_name=None, moving_variance_name=None, do_model_average_for_mean_and_var=False, fuse_with_relu=False, use_global_stats=False):
    "\n    **Batch Normalization Layer**\n\n    Can be used as a normalizer function for conv2d and fully_connected operations.\n    The required data format for this layer is one of the following:\n\n    1. NHWC `[batch, in_height, in_width, in_channels]`\n\n    2. NCHW `[batch, in_channels, in_height, in_width]`\n\n    Refer to `Batch Normalization: Accelerating Deep Network Training by Reducing\n    Internal Covariate Shift <https://arxiv.org/pdf/1502.03167.pdf>`_\n    for more details.\n\n    :math:`input` is the input features over a mini-batch.\n\n    ..  math::\n\n        \\mu_{\\beta} &\\gets \\frac{1}{m} \\sum_{i=1}^{m} x_i \\qquad &//\\\n        \\ mini-batch\\ mean \\\\\n        \\sigma_{\\beta}^{2} &\\gets \\frac{1}{m} \\sum_{i=1}^{m}(x_i - \\\n        \\mu_{\\beta})^2 \\qquad &//\\ mini-batch\\ variance \\\\\n        \\hat{x_i} &\\gets \\frac{x_i - \\mu_\\beta} {\\sqrt{\\\n        \\sigma_{\\beta}^{2} + \\epsilon}} \\qquad &//\\ normalize \\\\\n        y_i &\\gets \\gamma \\hat{x_i} + \\beta \\qquad &//\\ scale\\ and\\ shift\n\n\n    When use_global_stats = True, the :math:`\\mu_{\\beta}`\n    and :math:`\\sigma_{\\beta}^{2}` are not the statistics of one mini-batch.\n    They are global (or running) statistics. (It usually got from the\n    pre-trained model.)\n    The training and testing (or inference) have the same behavior:\n\n    ..  math::\n\n        \\hat{x_i} &\\gets \\frac{x_i - \\mu_\\beta} {\\sqrt{\\\n        \\sigma_{\\beta}^{2} + \\epsilon}}  \\\\\n        y_i &\\gets \\gamma \\hat{x_i} + \\beta\n\n    Args:\n        input(variable): The input variable which is a LoDTensor.\n        act(string, Default None): Activation type, linear|relu|prelu|...\n        is_test(bool, Default False): Used for training or training.\n        momentum(float, Default 0.9):\n        epsilon(float, Default 1e-05):\n        param_attr(ParamAttr|None): The parameter attribute for Parameter `scale`\n             of batch_norm. If it is set to None or one attribute of ParamAttr, batch_norm\n             will create ParamAttr as param_attr. If the Initializer of the param_attr\n             is not set, the parameter is initialized with Xavier. Default: None.\n        bias_attr(ParamAttr|None): The parameter attribute for the bias of batch_norm.\n             If it is set to None or one attribute of ParamAttr, batch_norm\n             will create ParamAttr as bias_attr. If the Initializer of the bias_attr\n             is not set, the bias is initialized zero. Default: None.\n        data_layout(string, default NCHW): NCHW|NHWC\n        in_place(bool, Default False): Make the input and output of batch norm reuse memory.\n        name(string, Default None): A name for this layer(optional). If set None, the layer\n            will be named automatically.\n        moving_mean_name(string, Default None): The name of moving_mean which store the global Mean.\n        moving_variance_name(string, Default None): The name of the moving_variance which store the global Variance.\n        do_model_average_for_mean_and_var(bool, Default False): Do model average for mean and variance or not.\n        fuse_with_relu (bool): if True, this OP performs relu after batch norm.\n        use_global_stats(bool, Default False): Whether to use global mean and\n            variance. In inference or test mode, set use_global_stats to true\n            or is_test to true, and the behavior is equivalent.\n            In train mode, when setting use_global_stats True, the global mean\n            and variance are also used during train period.\n\n    Returns:\n        Variable: A tensor variable which is the result after applying batch normalization on the input.\n\n    Examples:\n\n        .. code-block:: python\n\n            hidden1 = fluid.layers.fc(input=x, size=200, param_attr='fc1.w')\n            hidden2 = fluid.layers.batch_norm(input=hidden1)\n    "
    assert (bias_attr is not False), 'bias_attr should not be False in batch_norm.'
    helper = LayerHelper('batch_norm', **locals())
    dtype = helper.input_dtype()
    if (dtype == core.VarDesc.VarType.FP16):
        dtype = core.VarDesc.VarType.FP32
    input_shape = input.shape
    if (data_layout == 'NCHW'):
        channel_num = input_shape[1]
    elif (data_layout == 'NHWC'):
        channel_num = input_shape[(- 1)]
    else:
        raise ValueError(('unsupported data layout:' + data_layout))
    param_shape = [channel_num]
    scale = helper.create_parameter(attr=helper.param_attr, shape=param_shape, dtype=dtype, default_initializer=Constant(1.0))
    if (use_global_stats and (helper.param_attr.learning_rate == 0.0)):
        scale.stop_gradient = True
    bias = helper.create_parameter(attr=helper.bias_attr, shape=param_shape, dtype=dtype, is_bias=True)
    if (use_global_stats and (helper.bias_attr.learning_rate == 0.0)):
        bias.stop_gradient = True
    mean = helper.create_parameter(attr=ParamAttr(name=moving_mean_name, initializer=Constant(0.0), trainable=False, do_model_average=do_model_average_for_mean_and_var), shape=param_shape, dtype=dtype)
    mean.stop_gradient = True
    variance = helper.create_parameter(attr=ParamAttr(name=moving_variance_name, initializer=Constant(1.0), trainable=False, do_model_average=do_model_average_for_mean_and_var), shape=param_shape, dtype=dtype)
    variance.stop_gradient = True
    mean_out = mean
    variance_out = variance
    saved_mean = helper.create_variable_for_type_inference(dtype=dtype, stop_gradient=True)
    saved_variance = helper.create_variable_for_type_inference(dtype=dtype, stop_gradient=True)
    batch_norm_out = (input if in_place else helper.create_variable_for_type_inference(dtype))
    helper.append_op(type='batch_norm', inputs={
        'X': input,
        'Scale': scale,
        'Bias': bias,
        'Mean': mean,
        'Variance': variance,
    }, outputs={
        'Y': batch_norm_out,
        'MeanOut': mean_out,
        'VarianceOut': variance_out,
        'SavedMean': saved_mean,
        'SavedVariance': saved_variance,
    }, attrs={
        'momentum': momentum,
        'epsilon': epsilon,
        'is_test': is_test,
        'data_layout': data_layout,
        'use_mkldnn': False,
        'fuse_with_relu': fuse_with_relu,
        'use_global_stats': use_global_stats,
    })
    return helper.append_activation(batch_norm_out)