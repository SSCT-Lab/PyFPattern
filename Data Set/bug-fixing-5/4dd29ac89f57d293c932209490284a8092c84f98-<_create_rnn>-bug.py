@classmethod
def _create_rnn(cls, init_model, pred_model, n, opset_version):
    assert (init_model is not None), 'cannot convert RNNs without access to the full model'
    assert (pred_model is not None), 'cannot convert RNNs without access to the full model'
    attrs = dict(n.attrs)
    hidden_size = attrs.pop('hidden_size')
    activation = force_unicode(attrs.pop('activations', ('tanh',))[0])
    direction = force_unicode(attrs.pop('direction', 'forward'))
    assert (not attrs), ('unsupported RNN attributes: ' + str(attrs.keys()))
    assert (direction in ['forward', 'bidirectional']), 'unsupported backwards RNN'
    (input_blob, W, R, B, sequence_lens, initial_h) = n.inputs
    if (sequence_lens == ''):
        sequence_lens = None
    input_size = cls._rnn_shape_inference(init_model, pred_model, n, input_blob, W)
    if (input_size is None):
        raise RuntimeError('best-effort shape inference for RNN input failed')
    init_net = core.Net('init-net')
    pred_mh = ModelHelper()

    def make_rnn(direction_offset):
        name = cls.dummy_name()
        bias_offset = ((2 * direction_offset) * hidden_size)
        init_net.Slice(B, (name + '/i2h_b'), starts=[(bias_offset + (0 * hidden_size))], ends=[(bias_offset + (1 * hidden_size))])
        init_net.Slice(B, (name + '/gates_t_b'), starts=[(bias_offset + (1 * hidden_size))], ends=[(bias_offset + (2 * hidden_size))])
        weight_offset = (direction_offset * hidden_size)
        init_net.Slice(W, (name + '/i2h_w'), starts=[(weight_offset + (0 * hidden_size)), 0], ends=[(weight_offset + (1 * hidden_size)), (- 1)])
        init_net.Slice(R, (name + '/gates_t_w'), starts=[(weight_offset + (0 * hidden_size)), 0], ends=[(weight_offset + (1 * hidden_size)), (- 1)])
        initial_h_sliced = (name + '/initial_h')
        init_net.Slice(initial_h, initial_h_sliced, starts=[(direction_offset + 0), 0, 0], ends=[(direction_offset + 1), (- 1), (- 1)])
        if (direction_offset == 1):
            if (sequence_lens is not None):
                seq_lens_for_reverse = sequence_lens
            else:
                input_shape = pred_mh.net.Shape(input_blob, (name + '/input_shape'))
                batch_size = pred_mh.net.Slice(input_shape, (name + '/batch_size_slice'), starts=[1], ends=[2])
                seq_len = pred_mh.net.Slice(input_shape, (name + '/seq_len_slice'), starts=[0], ends=[1])
                dummy_sequence_lens = pred_mh.net.Tile([seq_len, batch_size], (name + '/dummy_sequence_lens'), axis=0)
                pred_mh.net.Reshape(dummy_sequence_lens, [dummy_sequence_lens, dummy_name()], shape=[(- 1)])
                seq_lens_for_reverse = dummy_sequence_lens
        if (direction_offset == 1):
            input = pred_mh.net.ReversePackedSegs([input_blob, seq_lens_for_reverse], (name + '/input-reversed'))
        else:
            input = input_blob
        (hidden_t_all, hidden_t_last) = rnn_cell.BasicRNN(pred_mh, input, sequence_lens, [initial_h_sliced], input_size, hidden_size, name, drop_states=False, forward_only=True, activation=activation)
        if (direction_offset == 1):
            hidden_t_all = pred_mh.net.ReversePackedSegs([hidden_t_all, seq_lens_for_reverse], (name + '/output-reversed'))
        return (hidden_t_all, hidden_t_last)
    if (direction == 'forward'):
        (hidden_t_all, hidden_t_last) = make_rnn(0)
        pred_mh.net.Copy(hidden_t_last, n.outputs[1])
        pred_mh.net = pred_mh.net.Clone('dummy-clone-net', blob_remap={
            hidden_t_all: n.outputs[0],
        })
    elif (direction == 'bidirectional'):
        (hidden_t_all_f, hidden_t_last_f) = make_rnn(0)
        (hidden_t_all_b, hidden_t_last_b) = make_rnn(1)
        pred_mh.net.Concat([hidden_t_all_f, hidden_t_all_b], [n.outputs[0], cls.dummy_name()], axis=2)
        pred_mh.net.Concat([hidden_t_last_f, hidden_t_last_b], [n.outputs[1], cls.dummy_name()], axis=0)
    if (sequence_lens is not None):
        pred_mh.net.VariableLengthSequencePadding([n.outputs[0], sequence_lens], [n.outputs[0]])
    return Caffe2Ops(list(pred_mh.Proto().op), list(init_net.Proto().op), list(pred_mh.Proto().external_input))