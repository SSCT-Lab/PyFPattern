def fc(input, size, num_flatten_dims=1, param_attr=None, bias_attr=None, act=None, name=None):
    '\n    **Fully Connected Layer**\n\n    The fully connected layer can take multiple tensors as its inputs. It\n    creates a variable (one for each input tensor) called weights for each\n    input tensor, which represents a fully connected weight matrix from\n    each input unit to each output unit. The fully connected layer\n    multiplies each input tensor with its coresponding weight to produce\n    an output Tensor. If multiple input tensors are given, the results of\n    multiple multiplications will be sumed up. If bias_attr is not None,\n    a biases variable will be created and added to the output. Finally,\n    if activation is not None, it will be applied to the output as well.\n\n    This process can be formulated as follows:\n\n    .. math::\n\n        Out = Act({\\sum_{i=0}^{N-1}X_iW_i + b})\n\n    In the above equation:\n\n    * :math:`N`: Number of the input.\n    * :math:`X_i`: The input tensor.\n    * :math:`W`: The weights created by this layer.\n    * :math:`b`: The bias parameter created by this layer (if needed).\n    * :math:`Act`: The activation funtion.\n    * :math:`Out`: The output tensor.\n\n    Args:\n       input(Variable|list): The input tensor(s) to the fully connected layer.\n       size(int): The number of output units in the fully connected layer.\n       num_flatten_dims(int): The fc layer can accept an input tensor with more\n                              than two dimensions. If this happens, the\n                              multidimensional tensor will first be flattened\n                              into a 2-dimensional matrix. The parameter\n                              `num_flatten_dims` determines how the input tensor\n                              is flattened: the first `num_flatten_dims`\n                              (inclusive, index starts from 1) dimensions will\n                              be flatten to form the first dimension of the\n                              final matrix (height of the matrix), and the rest\n                              `rank(X) - num_flatten_dims` dimensions are\n                              flattened to form the second dimension of the\n                              final matrix (width of the matrix). For example,\n                              suppose `X` is a 6-dimensional tensor with a shape\n                              [2, 3, 4, 5, 6], and `num_flatten_dims` = 3. Then,\n                              the flattened matrix will have a shape\n                              [2 x 3 x 4, 5 x 6] = [24, 30]. By default,\n                              `num_flatten_dims` is set to 1.\n       param_attr(ParamAttr|list): The parameter attribute for learnable\n                                   parameters/weights of the fully connected\n                                   layer.\n       param_initializer(ParamAttr|list): The initializer used for the\n                                          weight/parameter. If set None,\n                                          XavierInitializer() will be used.\n       bias_attr(ParamAttr|list): The parameter attribute for the bias parameter\n                                  for this layer. If set None, no bias will be\n                                  added to the output units.\n       bias_initializer(ParamAttr|list): The initializer used for the bias.\n                                        If set None, then ConstantInitializer()\n                                        will be used.\n       act(str): Activation to be applied to the output of the fully connected\n                 layer.\n       name(str): Name/alias of the fully connected layer.\n\n\n    Returns:\n        Variable: The output tensor variable.\n\n    Raises:\n        ValueError: If rank of the input tensor is less than 2.\n\n    Examples:\n        .. code-block:: python\n\n          data = fluid.layers.data(name="data", shape=[32, 32], dtype="float32")\n          fc = fluid.layers.fc(input=data, size=1000, act="tanh")\n    '
    helper = LayerHelper('fc', **locals())
    dtype = helper.input_dtype()
    mul_results = []
    for (input_var, param_attr) in helper.iter_inputs_and_params():
        input_shape = input_var.shape
        param_shape = ([reduce((lambda a, b: (a * b)), input_shape[num_flatten_dims:], 1)] + [size])
        w = helper.create_parameter(attr=param_attr, shape=param_shape, dtype=dtype, is_bias=False)
        tmp = helper.create_tmp_variable(dtype)
        helper.append_op(type='mul', inputs={
            'X': input_var,
            'Y': w,
        }, outputs={
            'Out': tmp,
        }, attrs={
            'x_num_col_dims': num_flatten_dims,
            'y_num_col_dims': 1,
        })
        mul_results.append(tmp)
    if (len(mul_results) == 1):
        pre_bias = mul_results[0]
    else:
        pre_bias = helper.create_tmp_variable(dtype)
        helper.append_op(type='sum', inputs={
            'X': mul_results,
        }, outputs={
            'Out': pre_bias,
        })
    pre_activation = helper.append_bias_op(pre_bias, dim_start=num_flatten_dims)
    return helper.append_activation(pre_activation)