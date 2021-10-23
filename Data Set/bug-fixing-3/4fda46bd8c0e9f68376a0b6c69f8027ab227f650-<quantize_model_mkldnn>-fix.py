def quantize_model_mkldnn(sym, arg_params, aux_params, data_names=('data',), label_names=('softmax_label',), ctx=cpu(), excluded_sym_names=None, excluded_op_names=None, calib_mode='entropy', calib_data=None, num_calib_examples=None, quantized_dtype='int8', quantize_mode='smart', logger=None):
    'User-level API for generating a fusion + quantized model from a FP32 model\n    w/ or w/o calibration with Intel MKL-DNN.\n    The backend quantized operators are only enabled for Linux systems. Please do not run\n    inference using the quantized models on Windows for now.\n\n    Parameters\n    ----------\n    same with quantize_model\n\n    Returns\n    -------\n    tuple\n        A tuple of quantized symbol, quantized arg_params, and aux_params.\n    -------\n    '
    if (not isinstance(ctx, Context)):
        raise ValueError(('currently only supports single ctx, while received %s' % str(ctx)))
    if (ctx.device_type != 'cpu'):
        raise ValueError('quantize_model_mkldnn only support Intel cpu platform with MKL-DNN Backend')
    sym = sym.get_backend_symbol('MKLDNN_QUANTIZE')
    (qsym, qarg_params, aux_params) = quantize_model(sym=sym, arg_params=arg_params, aux_params=aux_params, data_names=data_names, label_names=label_names, ctx=ctx, excluded_sym_names=excluded_sym_names, excluded_op_names=excluded_op_names, calib_mode=calib_mode, calib_data=calib_data, num_calib_examples=num_calib_examples, quantized_dtype=quantized_dtype, quantize_mode=quantize_mode, logger=logger)
    qsym = qsym.get_backend_symbol('MKLDNN_QUANTIZE')
    return (qsym, qarg_params, aux_params)