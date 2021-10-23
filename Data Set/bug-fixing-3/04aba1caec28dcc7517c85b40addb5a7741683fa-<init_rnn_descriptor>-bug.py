def init_rnn_descriptor(fn, handle):
    return cudnn.RNNDescriptor(handle, fn.hidden_size, fn.num_layers, fn.dropout_state['desc'].get(), fn.input_mode, fn.bidirectional, fn.mode, fn.datatype)