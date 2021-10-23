def get_parameters(fn, handle, weight_buf):
    'Returns weight and bias tensors for each layer of the RNN. These tensors\n    are views on the underlying weight buffer allocated by CuDNN.\n\n    Note: for LSTM and GRU, which have multiple parameters of each type (4 and 3, respectively),\n          these parameters are concatenated along the first dimension.\n          These parameters are returned in a consistent order by CuDNN:\n              (reset, forget, cell, outut) for LSTM\n              (reset, input, new) for GRU\n    Args:\n        fn: The RNN function object holding the RNN state\n        handle: a CuDNN handle\n        weight_buf: a 1D tensor containing the CuDNN-allocated weight (or grad_weight) buffer\n    Returns:\n        parameters: [(weight_ih, weight_hh, bias_ih, bias_hh)*], with length equal to the num_layers.\n    '
    cudnn_methods = [cudnn.lib.cudnnGetRNNLinLayerMatrixParams, cudnn.lib.cudnnGetRNNLinLayerBiasParams]
    params = []
    num_linear_layers = _num_linear_layers(fn)
    num_layers = (fn.num_directions * fn.num_layers)
    for layer in range(num_layers):
        layer_params = []
        for cudnn_method in cudnn_methods:
            for linear_id in range(num_linear_layers):
                lin_layer_mat_desc = cudnn.FilterDescriptor()
                matrix_pointer = ctypes.c_void_p()
                check_error(cudnn_method(handle, fn.rnn_desc, layer, fn.x_descs[0], fn.w_desc, ctypes.c_void_p(weight_buf.data_ptr()), linear_id, lin_layer_mat_desc, ctypes.byref(matrix_pointer)))
                data_type = ctypes.c_int()
                format = ctypes.c_int()
                nb_dims = ctypes.c_int()
                min_dim = 3
                filter_dim_a = torch.IntTensor(min_dim)
                check_error(cudnn.lib.cudnnGetFilterNdDescriptor(lin_layer_mat_desc, min_dim, ctypes.byref(data_type), ctypes.byref(format), ctypes.byref(nb_dims), ctypes.c_void_p(filter_dim_a.data_ptr())))
                assert (nb_dims.value <= min_dim)
                filter_dim_a = filter_dim_a[:nb_dims.value]
                elem_size = cudnn._sizeofmap[fn.datatype]
                offset_bytes = (matrix_pointer.value - weight_buf.data_ptr())
                assert ((offset_bytes % elem_size) == 0)
                offset = (offset_bytes // elem_size)
                if ((linear_id == 0) or (linear_id == (num_linear_layers / 2))):
                    assert (filter_dim_a.prod() == filter_dim_a[0])
                    param = fn.weight_buf.new().set_(weight_buf.storage(), offset, ((filter_dim_a[0] * num_linear_layers) // 2), filter_dim_a[2])
                    layer_params.append(param)
                else:
                    assert (cur_offset == offset)
                cur_offset = (offset + filter_dim_a[0])
        params.append(layer_params)
    return params