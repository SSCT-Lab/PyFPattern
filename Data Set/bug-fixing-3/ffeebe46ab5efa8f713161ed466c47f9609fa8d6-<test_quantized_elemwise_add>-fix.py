@with_seed()
def test_quantized_elemwise_add():

    def check_quantized_elemwise_add(data_shape, qtype):
        if is_test_for_native_cpu():
            print('skipped testing quantized_elemwise_add for native cpu since it is not supported yet')
            return
        elif ((qtype != 'uint8') and (qtype != 'int8')):
            print('skipped testing quantized_elemwise_add for not supported data type')
            return
        elif is_test_for_gpu():
            print('skipped testing quantized_elemwise_add for gpu since it is not supported yet')
            return
        dataA = mx.sym.Variable(name='dataA', shape=data_shape, dtype='float32')
        dataB = mx.sym.Variable(name='dataB', shape=data_shape, dtype='float32')
        elemwise_add_fp32 = mx.sym.elemwise_add(dataA, dataB)
        arg_names = elemwise_add_fp32.list_arguments()
        elemwise_add_fp32_exe = elemwise_add_fp32.simple_bind(ctx=mx.current_context(), grad_req='null')
        if (qtype == 'uint8'):
            data_low = 0.0
            data_high = 255.0
        else:
            data_low = (- 127.0)
            data_high = 127.0
        dataA_val = mx.nd.random.uniform(low=data_low, high=data_high, shape=data_shape).astype('int32')
        dataB_val = mx.nd.random.uniform(low=data_low, high=data_high, shape=data_shape).astype('int32')
        elemwise_add_fp32_exe.arg_dict[arg_names[0]][:] = dataA_val
        elemwise_add_fp32_exe.arg_dict[arg_names[1]][:] = dataB_val
        output = elemwise_add_fp32_exe.forward()[0]
        qdataA = mx.sym.Variable(name='qdataA', shape=data_shape, dtype=qtype)
        qdataB = mx.sym.Variable(name='qdataB', shape=data_shape, dtype=qtype)
        min_dataA = mx.sym.Variable(name='min_dataA')
        max_dataA = mx.sym.Variable(name='max_dataA')
        min_dataB = mx.sym.Variable(name='min_dataB')
        max_dataB = mx.sym.Variable(name='max_dataB')
        quantized_elemwise_add = mx.sym.contrib.quantized_elemwise_add(qdataA, qdataB, min_dataA, max_dataA, min_dataB, max_dataB)
        elemwise_add_int8_exe = quantized_elemwise_add.simple_bind(ctx=mx.current_context(), grad_req='null')
        qarg_names = quantized_elemwise_add.list_arguments()
        elemwise_add_int8_exe.arg_dict[qarg_names[0]][:] = elemwise_add_fp32_exe.arg_dict[arg_names[0]].astype(qtype)
        elemwise_add_int8_exe.arg_dict[qarg_names[1]][:] = elemwise_add_fp32_exe.arg_dict[arg_names[1]].astype(qtype)
        quantized_range = 127.0
        elemwise_add_int8_exe.arg_dict[qarg_names[2]][:] = data_low
        elemwise_add_int8_exe.arg_dict[qarg_names[3]][:] = data_high
        elemwise_add_int8_exe.arg_dict[qarg_names[4]][:] = data_low
        elemwise_add_int8_exe.arg_dict[qarg_names[5]][:] = data_high
        (qoutput, min_range, max_range) = elemwise_add_int8_exe.forward()
        int8_rslt = ((qoutput.astype(output.dtype) * max_range) / 2147483647)
        diff = mx.nd.abs((output - int8_rslt))
        cond = mx.nd.lesser(2, diff).sum().asscalar()
        assert (cond == 0)
    for qtype in ['int8', 'uint8']:
        check_quantized_elemwise_add((4, 6), qtype)
        check_quantized_elemwise_add((13, 74, 52), qtype)
        check_quantized_elemwise_add((3, 4, 56, 56), qtype)
        check_quantized_elemwise_add((32, 56, 64, 11), qtype)