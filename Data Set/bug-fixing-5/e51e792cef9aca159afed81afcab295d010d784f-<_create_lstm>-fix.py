@classmethod
def _create_lstm(cls, init_model, pred_model, n, opset_version):
    assert (init_model is not None), 'cannot convert LSTMs without access to the full model'
    assert (pred_model is not None), 'cannot convert LSTMs without access to the full model'
    attrs = dict(n.attrs)
    hidden_size = attrs.pop('hidden_size')
    direction = force_unicode(attrs.pop('direction', 'forward'))
    assert (not attrs), ('unsupported LSTM attributes: ' + str(attrs.keys()))
    assert (direction in ['forward', 'bidirectional']), 'unsupported backwards LSTM'
    (input_blob, W, R, B, sequence_lens, initial_h, initial_c) = n.inputs
    if (sequence_lens == ''):
        sequence_lens = None
    input_size = cls._rnn_shape_inference(init_model, pred_model, n, input_blob, W)
    if (input_size is None):
        raise RuntimeError('best-effort shape inference for LSTM input failed')
    init_net = core.Net('init-net')
    pred_mh = ModelHelper()

    def make_lstm(direction_offset):
        name = cls.dummy_name()
        bias_offset = ((8 * direction_offset) * hidden_size)
        Bi = init_net.Slice(B, (name + '_bias_i2h'), starts=[(bias_offset + (0 * hidden_size))], ends=[(bias_offset + (4 * hidden_size))])
        Br = init_net.Slice(B, (name + '_bias_gates'), starts=[(bias_offset + (4 * hidden_size))], ends=[(bias_offset + (8 * hidden_size))])
        weight_offset = ((4 * direction_offset) * hidden_size)
        W_ = init_net.Slice(W, (name + '/i2h_w_pre'), starts=[(weight_offset + (0 * hidden_size)), 0], ends=[(weight_offset + (4 * hidden_size)), (- 1)])
        R_ = init_net.Slice(R, (name + '/gates_t_w_pre'), starts=[(weight_offset + (0 * hidden_size)), 0], ends=[(weight_offset + (4 * hidden_size)), (- 1)])
        reforms = ((W_, 'i2h_w', [(0, (- 1))]), (R_, 'gates_t_w', [(0, (- 1))]), (Bi, 'i2h_b', []), (Br, 'gates_t_b', []))
        for (name_from, name_to, extra_dims) in reforms:
            (xi, xo, xf, xc) = [(name_from + suffix) for suffix in ('_i', '_o', '_f', '_c')]
            for (i, x) in enumerate([xi, xo, xf, xc]):
                dim0 = ((i * hidden_size), ((i + 1) * hidden_size))
                (starts, ends) = zip(dim0, *extra_dims)
                init_net.Slice(name_from, x, starts=starts, ends=ends)
            init_net.Concat([xi, xf, xo, xc], [('%s/%s' % (name, name_to)), cls.dummy_name()], axis=0)
        initial_h_sliced = (name + '/initial_h')
        init_net.Slice(initial_h, initial_h_sliced, starts=[(direction_offset + 0), 0, 0], ends=[(direction_offset + 1), (- 1), (- 1)])
        initial_c_sliced = (name + '/initial_c')
        init_net.Slice(initial_c, initial_c_sliced, starts=[(direction_offset + 0), 0, 0], ends=[(direction_offset + 1), (- 1), (- 1)])
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
        (hidden_t_all, hidden_t_last, _, cell_last, params) = rnn_cell.LSTM(pred_mh, input, sequence_lens, [initial_h_sliced, initial_c_sliced], input_size, hidden_size, name, drop_states=False, forward_only=True, return_params=True)
        if (direction_offset == 1):
            hidden_t_all = pred_mh.net.ReversePackedSegs([hidden_t_all, seq_lens_for_reverse], (name + '/output-reversed'))
        return (hidden_t_all, hidden_t_last, cell_last)
    if (direction == 'forward'):
        (hidden_t_all, hidden_t_last, cell_last) = make_lstm(0)
        pred_mh.net.Copy(hidden_t_last, n.outputs[1])
        pred_mh.net.Copy(cell_last, n.outputs[2])
        pred_mh.net = pred_mh.net.Clone('dummy-clone-net', blob_remap={
            hidden_t_all: n.outputs[0],
        })
    elif (direction == 'bidirectional'):
        (hidden_t_all_f, hidden_t_last_f, cell_last_f) = make_lstm(0)
        (hidden_t_all_b, hidden_t_last_b, cell_last_b) = make_lstm(1)
        pred_mh.net.Concat([hidden_t_all_f, hidden_t_all_b], [n.outputs[0], cls.dummy_name()], axis=2)
        pred_mh.net.Concat([hidden_t_last_f, hidden_t_last_b], [n.outputs[1], cls.dummy_name()], axis=0)
        pred_mh.net.Concat([cell_last_f, cell_last_b], [n.outputs[2], cls.dummy_name()], axis=0)
    if (sequence_lens is not None):
        pred_mh.net.VariableLengthSequencePadding([n.outputs[0], sequence_lens], [n.outputs[0]])
    return Caffe2Ops(list(pred_mh.Proto().op), list(init_net.Proto().op), list(pred_mh.Proto().external_input))