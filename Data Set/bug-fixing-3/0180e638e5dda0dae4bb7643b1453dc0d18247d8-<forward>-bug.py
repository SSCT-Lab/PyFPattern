def forward(fn, input, hx, weight, output, hy):
    with torch.cuda.device_of(input):
        lib = cudnn.lib
        handle = cudnn.get_handle()
        fn.datatype = cudnn._typemap[input.type()]
        if (fn.mode == cudnn.CUDNN_LSTM):
            (hx, cx) = hx
            (hy, cy) = hy
        else:
            (cx, cy) = (None, None)
        if fn.batch_first:
            input = input.transpose(0, 1)
        if (input.dim() != 3):
            raise RuntimeError('input must have 3 dimensions, got {}'.format(input.dim()))
        if (fn.input_size != input.size(2)):
            raise RuntimeError('input.size(2) must be equal to input_size. Expected {}, got {}'.format(fn.input_size))
        if ((fn.dropout != 0) and (cudnn.version() < 5103)):
            raise RuntimeError('dropout supported only in cudnn v5.1 and above')
        (fn.seq_length, fn.mini_batch, fn.input_size) = input.size()
        hidden_size = _hidden_size(fn)
        output_size = _output_size(fn)
        x = input.contiguous()
        output.resize_(*output_size)
        hy.resize_(*hidden_size).zero_()
        if (cy is not None):
            cy.resize_(*hidden_size).zero_()
        y = output
        if (('desc' not in fn.dropout_state) or (fn.dropout_state['desc'].get() is None)):
            fn.dropout_state['desc'] = Unserializable(init_dropout_descriptor(fn, handle))
        fn.rnn_desc = init_rnn_descriptor(fn)
        fn.x_descs = cudnn.descriptor(x[0], fn.seq_length)
        fn.y_descs = cudnn.descriptor(y[0], fn.seq_length)
        fn.hx_desc = cudnn.descriptor(hx)
        fn.hy_desc = cudnn.descriptor(hx)
        fn.cx_desc = (cudnn.descriptor(cx) if (cx is not None) else None)
        fn.cy_desc = (cudnn.descriptor(cx) if (cx is not None) else None)
        num_weights = get_num_weights(handle, fn.rnn_desc, fn.x_descs[0], fn.datatype)
        fn.weight_buf = input.new(num_weights)
        fn.w_desc = init_weight_descriptor(fn, fn.weight_buf)
        w = fn.weight_buf
        w.zero_()
        params = get_parameters(fn, handle, w)
        _copyParams(weight, params)
        if (tuple(hx.size()) != hidden_size):
            raise RuntimeError('Expected hidden size {}, got {}'.format(hidden_size, tuple(hx.size())))
        if ((cx is not None) and (tuple(cx.size()) != hidden_size)):
            raise RuntimeError('Expected cell size {}, got {}'.format(hidden_size, tuple(cx.size())))
        workspace_size = ctypes.c_long()
        check_error(lib.cudnnGetRNNWorkspaceSize(handle, fn.rnn_desc, fn.seq_length, fn.x_descs, ctypes.byref(workspace_size)))
        fn.workspace = torch.cuda.ByteTensor(workspace_size.value)
        if fn.train:
            reserve_size = ctypes.c_long()
            check_error(lib.cudnnGetRNNTrainingReserveSize(handle, fn.rnn_desc, fn.seq_length, fn.x_descs, ctypes.byref(reserve_size)))
            fn.reserve = torch.cuda.ByteTensor(reserve_size.value)
            check_error(lib.cudnnRNNForwardTraining(handle, fn.rnn_desc, fn.seq_length, fn.x_descs, ctypes.c_void_p(x.data_ptr()), fn.hx_desc, ctypes.c_void_p(hx.data_ptr()), fn.cx_desc, (ctypes.c_void_p(cx.data_ptr()) if (cx is not None) else None), fn.w_desc, ctypes.c_void_p(w.data_ptr()), fn.y_descs, ctypes.c_void_p(y.data_ptr()), fn.hy_desc, ctypes.c_void_p(hy.data_ptr()), fn.cy_desc, (ctypes.c_void_p(cy.data_ptr()) if (cx is not None) else None), ctypes.c_void_p(fn.workspace.data_ptr()), fn.workspace.size(0), ctypes.c_void_p(fn.reserve.data_ptr()), fn.reserve.size(0)))
        else:
            check_error(lib.cudnnRNNForwardInference(handle, fn.rnn_desc, fn.seq_length, fn.x_descs, ctypes.c_void_p(x.data_ptr()), fn.hx_desc, ctypes.c_void_p(hx.data_ptr()), fn.cx_desc, (ctypes.c_void_p(cx.data_ptr()) if (cx is not None) else None), fn.w_desc, ctypes.c_void_p(w.data_ptr()), fn.y_descs, ctypes.c_void_p(y.data_ptr()), fn.hy_desc, ctypes.c_void_p(hy.data_ptr()), fn.cy_desc, (ctypes.c_void_p(cy.data_ptr()) if (cx is not None) else None), ctypes.c_void_p(fn.workspace.data_ptr()), fn.workspace.size(0)))
        if fn.batch_first:
            output = output.transpose_(0, 1)