def flatten_parameters(self):
    "Resets parameter data pointer so that they can use faster code paths.\n\n        Right now, this works only if the module is on the GPU and cuDNN is enabled.\n        Otherwise, it's a no-op.\n        "
    any_param = next(self.parameters()).data
    if ((not any_param.is_cuda) or (not torch.backends.cudnn.is_acceptable(any_param))):
        self._data_ptrs = []
        return
    from torch.backends.cudnn import rnn
    from torch.backends import cudnn
    from torch.nn._functions.rnn import CudnnRNN
    handle = cudnn.get_handle()
    with warnings.catch_warnings(record=True):
        fn = CudnnRNN(self.mode, self.input_size, self.hidden_size, num_layers=self.num_layers, batch_first=self.batch_first, dropout=self.dropout, train=self.training, bidirectional=self.bidirectional, dropout_state=self.dropout_state)
    fn.datatype = cudnn._typemap[any_param.type()]
    fn.x_descs = cudnn.descriptor(any_param.new(1, self.input_size), 1)
    fn.rnn_desc = rnn.init_rnn_descriptor(fn, handle)
    num_weights = rnn.get_num_weights(handle, fn.rnn_desc, fn.x_descs[0], fn.datatype)
    fn.weight_buf = any_param.new(num_weights).zero_()
    fn.w_desc = rnn.init_weight_descriptor(fn, fn.weight_buf)
    params = rnn.get_parameters(fn, handle, fn.weight_buf)
    all_weights = [[p.data for p in l] for l in self.all_weights]
    rnn._copyParams(all_weights, params)
    for (orig_layer_param, new_layer_param) in zip(all_weights, params):
        for (orig_param, new_param) in zip(orig_layer_param, new_layer_param):
            orig_param.set_(new_param.view_as(orig_param))
    self._data_ptrs = list((p.data.data_ptr() for p in self.parameters()))