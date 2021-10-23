

def Print(input, first_n=(- 1), message=None, summarize=20, print_tensor_name=True, print_tensor_type=True, print_tensor_shape=True, print_tensor_lod=True, print_phase='both'):
    '\n    **Print operator**\n\n    This creates a print op that will print when a tensor is accessed.\n\n    Wraps the tensor passed in so that whenever that a tensor is accessed,\n    the message `message` is printed, along with the current value of the\n    tensor `t`.\n\n    Args:\n        input (Variable): A Tensor to print.\n        summarize (int): Number of elements in the tensor to be print. If it\'s\n                vaule is -1, then all elements in the tensor will be print.\n        message (str): A string message to print as a prefix.\n        first_n (int): Only log `first_n` number of times.\n        print_tensor_name (bool, optional): Print the tensor name. Default: True.\n        print_tensor_type (bool, optional): Print the tensor type. Defaultt: True.\n        print_tensor_shape (bool, optional): Print the tensor shape. Default: True.\n        print_tensor_lod (bool, optional): Print the tensor lod. Default: True.\n        print_phase (str): Which phase to displace, including \'forward\',\n                \'backward\' and \'both\'. Default: \'both\'. If set to \'backward\', will \n                only print the gradients of input tensor; If set to \'both\', will\n                both print the input tensor itself and the gradients of input tensor.\n\n    Returns:\n        Variable: Output tensor.\n\n    NOTES:\n        The input and output are two different variables, and in the\n        following process, you should use the output variable but not the input,\n        otherwise, the print layer doesn\'t have backward.\n\n    Examples:\n        .. code-block:: python\n           \n           import paddle.fluid as fluid\n           \n           input = fluid.layers.fill_constant(shape=[10,2], value=3, dtype=\'int64\')\n           input = fluid.layers.Print(input, message="The content of input layer:")\n           \n           main_program = fluid.default_main_program()\n           exe = fluid.Executor(fluid.CPUPlace())\n           exe.run(main_program)\n\n    Output at runtime:\n        .. code-block:: bash \n           \n           The content of input layer:     The place is:CPUPlace\n           Tensor[fill_constant_0.tmp_0]\n               shape: [10,2,]\n               dtype: x\n               data: 3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3, \n               \n    '
    check_type_and_dtype(input, 'input', Variable, ['float32', 'float64', 'int32_t', 'int64_t', 'bool'], 'fluid.layers.Print')
    helper = LayerHelper((('print' + '_') + input.name), **locals())
    output = helper.create_variable_for_type_inference(input.dtype)
    helper.append_op(type='print', inputs={
        'In': input,
    }, outputs={
        'Out': output,
    }, attrs={
        'first_n': first_n,
        'summarize': summarize,
        'message': (message or ''),
        'print_tensor_name': print_tensor_name,
        'print_tensor_type': print_tensor_type,
        'print_tensor_shape': print_tensor_shape,
        'print_tensor_lod': print_tensor_lod,
        'print_phase': print_phase.upper(),
    })
    return output
