def bi_lstm_encoder(input_seq, hidden_size):
    input_forward_proj = fluid.layers.fc(input=input_seq, size=(hidden_size * 4), bias_attr=True)
    (forward, _) = fluid.layers.dynamic_lstm(input=input_forward_proj, size=(hidden_size * 4), use_peepholes=USE_PEEPHOLES)
    input_backward_proj = fluid.layers.fc(input=input_seq, size=(hidden_size * 4), bias_attr=True)
    (backward, _) = fluid.layers.dynamic_lstm(input=input_backward_proj, size=(hidden_size * 4), is_reverse=True, use_peepholes=USE_PEEPHOLES)
    forward_last = fluid.layers.sequence_last_step(input=forward)
    backward_first = fluid.layers.sequence_first_step(input=backward)
    return (forward_last, backward_first)