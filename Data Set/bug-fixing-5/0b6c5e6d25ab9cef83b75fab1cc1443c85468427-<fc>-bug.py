def fc(input, size, num_flatten_dims=1, param_attr=None, bias_attr=None, act=None, name=None):
    '\n    **Fully Connected Layer**\n\n    The fully connected layer can take multiple tensors as its inputs. It\n    creates a variable (one for each input tensor) called weights for each input\n    tensor, which represents a fully connected weight matrix from each input\n    unit to each output unit. The fully connected layer multiplies each input\n    tensor with its coresponding weight to produce an output Tensor. If\n    multiple input tensors are given, the results of multiple multiplications\n    will be sumed up. If bias_attr is not None, a biases variable will be\n    created and added to the output. Finally, if activation is not None,\n    it will be applied to the output as well.\n\n    This process can be formulated as follows:\n\n    .. math::\n\n        Out = Act({\\sum_{i=0}^{N-1}W_iX_i + b})\n\n    In the above equation:\n\n    * :math:`N`: Number of the input.\n    * :math:`X_i`: The input tensor.\n    * :math:`W`: The weights created by this layer.\n    * :math:`b`: The bias parameter created by this layer (if needed).\n    * :math:`Act`: The activation funtion.\n    * :math:`Out`: The output tensor.\n\n    Args:\n       input(Variable|list): The input tensor(s) to the fully connected layer.\n       size(int): The number of output units in the fully connected layer.\n       num_flatten_dims(int): The fc layer can accept an input tensor with more\n                              than two dimensions. If this happens, the\n                              multidimensional tensor will first be flattened\n                              into a 2-dimensional matrix. The parameter\n                              `num_flatten_dims` determines how the input tensor\n                              is flattened: the first `num_flatten_dims`\n                              dimensions will be flatten to form the first\n                              dimension of the final matrix (height of the\n                              matrix), and the rest `rank(X) - num_col_dims`\n                              dimensions are flattened to form the second\n                              dimension of the final matrix (width of the matrix).\n                              For example, suppose `X` is a 6-dimensional tensor\n                              with a shape [2, 3, 4, 5, 6], and\n                              `x_num_col_dims` = 3. Then, the flattened matrix\n                              will have a shape [2 x 3 x 4, 5 x 6] = [24, 30].\n                              By default, `x_num_col_dims` is set to 1.\n       param_attr(ParamAttr|list): The parameter attribute for learnable\n                                   parameters/weights of the fully connected\n                                   layer.\n       param_initializer(ParamAttr|list): The initializer used for the\n                                          weight/parameter. If set None,\n                                          XavierInitializer() will be used.\n       bias_attr(ParamAttr|list): The parameter attribute for the bias parameter\n                                  for this layer. If set None, no bias will be\n                                  added to the output units.\n       bias_initializer(ParamAttr|list): The initializer used for the bias.\n                                        If set None, then ConstantInitializer()\n                                        will be used.\n       act(str): Activation to be applied to the output of the fully connected\n                 layer.\n       name(str): Name/alias of the fully connected layer.\n\n\n    Returns:\n        Variable: The output tensor variable.\n\n    Raises:\n        ValueError: If rank of the input tensor is less than 2.\n\n    Examples:\n        .. code-block:: python\n\n          data = fluid.layers.data(name="data", shape=[32, 32], dtype="float32")\n          fc = fluid.layers.fc(input=data, size=1000, act="tanh")\n    '
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
    pre_activation = helper.append_bias_op(pre_bias)
    return helper.append_activation(pre_activation)