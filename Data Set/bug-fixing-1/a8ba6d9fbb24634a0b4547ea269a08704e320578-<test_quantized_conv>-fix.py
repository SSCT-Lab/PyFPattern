

@with_seed()
def test_quantized_conv():

    def check_quantized_conv(data_shape, kernel, num_filter, pad, stride, no_bias, qdtype):
        if is_test_for_native_cpu():
            print('skipped testing quantized_conv for native cpu since it is not supported yet')
            return
        elif ((qdtype == 'int8') and is_test_for_mkldnn()):
            print('skipped testing quantized_conv for mkldnn cpu int8 since it is not supported yet')
            return
        elif ((qdtype == 'uint8') and is_test_for_gpu()):
            print('skipped testing quantized_conv for gpu uint8 since it is not supported yet')
            return
        data = mx.sym.Variable(name='data', shape=data_shape, dtype='float32')
        conv2d = mx.sym.Convolution(data=data, kernel=kernel, num_filter=num_filter, pad=pad, stride=stride, no_bias=no_bias, cudnn_off=False, name='conv2d')
        (arg_shapes, _, _) = conv2d.infer_shape(data=data_shape)
        arg_names = conv2d.list_arguments()
        conv_exe_fp32 = conv2d.simple_bind(ctx=mx.current_context(), grad_req='null')
        if (qdtype == 'uint8'):
            data_low = 0.0
            data_high = 127.0
        else:
            data_low = (- 127.0)
            data_high = 127.0
        conv_exe_fp32.arg_dict[arg_names[0]][:] = mx.nd.random.uniform(low=data_low, high=data_high, shape=data_shape).astype('int32')
        conv_exe_fp32.arg_dict[arg_names[1]][:] = mx.nd.random.uniform(low=(- 127.0), high=127.0, shape=arg_shapes[1]).astype('int32')
        if (not no_bias):
            conv_exe_fp32.arg_dict[arg_names[2]][:] = mx.nd.random.uniform(low=(- 127.0), high=127.0, shape=arg_shapes[2]).astype('int32')
        output = conv_exe_fp32.forward()[0]
        qdata = mx.sym.Variable(name='qdata', shape=data_shape, dtype=qdtype)
        qweight = mx.sym.Variable(name='qweight', dtype='int8')
        min_data = mx.sym.Variable(name='min_data')
        max_data = mx.sym.Variable(name='max_data')
        min_weight = mx.sym.Variable(name='min_weight')
        max_weight = mx.sym.Variable(name='max_weight')
        quantized_conv2d = mx.sym.contrib.quantized_conv(data=qdata, weight=qweight, min_data=min_data, max_data=max_data, min_weight=min_weight, max_weight=max_weight, kernel=kernel, num_filter=num_filter, pad=pad, stride=stride, no_bias=no_bias)
        qarg_names = quantized_conv2d.list_arguments()
        type_dict = None
        if (not no_bias):
            type_dict = {
                qarg_names[2]: 'int8',
            }
        conv_exe_int8 = quantized_conv2d.simple_bind(ctx=mx.current_context(), type_dict=type_dict, grad_req='null')
        conv_exe_int8.arg_dict[qarg_names[0]][:] = conv_exe_fp32.arg_dict[arg_names[0]].astype(qdtype)
        conv_exe_int8.arg_dict[qarg_names[1]][:] = conv_exe_fp32.arg_dict[arg_names[1]].astype('int8')
        quantized_range = 127.0
        if no_bias:
            conv_exe_int8.arg_dict[qarg_names[2]][:] = (- quantized_range)
            conv_exe_int8.arg_dict[qarg_names[3]][:] = quantized_range
            conv_exe_int8.arg_dict[qarg_names[4]][:] = (- quantized_range)
            conv_exe_int8.arg_dict[qarg_names[5]][:] = quantized_range
        else:
            conv_exe_int8.arg_dict[qarg_names[2]][:] = conv_exe_fp32.arg_dict[arg_names[2]].astype('int8')
            conv_exe_int8.arg_dict[qarg_names[3]][:] = (- quantized_range)
            conv_exe_int8.arg_dict[qarg_names[4]][:] = quantized_range
            conv_exe_int8.arg_dict[qarg_names[5]][:] = (- quantized_range)
            conv_exe_int8.arg_dict[qarg_names[6]][:] = quantized_range
            conv_exe_int8.arg_dict[qarg_names[7]][:] = (- quantized_range)
            conv_exe_int8.arg_dict[qarg_names[8]][:] = quantized_range
        (qoutput, min_range, max_range) = conv_exe_int8.forward()
        if no_bias:
            assert_almost_equal(output.asnumpy(), qoutput.asnumpy(), atol=1)
        else:
            diff = mx.nd.abs((output - qoutput.astype(output.dtype)))
            cond = mx.nd.lesser(2, diff).sum().asscalar()
            assert (cond == 0)
    for qdtype in ['int8', 'uint8']:
        check_quantized_conv((3, 4, 28, 28), (3, 3), 128, (1, 1), (1, 1), True, qdtype)
        check_quantized_conv((3, 4, 28, 28), (3, 3), 128, (1, 1), (1, 1), False, qdtype)
