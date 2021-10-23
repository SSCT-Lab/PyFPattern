def seq_to_seq_net():
    'Construct a seq2seq network.'
    src_word_idx = fluid.layers.data(name='source_sequence', shape=[1], dtype='int64', lod_level=1)
    src_embedding = fluid.layers.embedding(input=src_word_idx, size=[source_dict_dim, embedding_dim], dtype='float32')
    (src_forward, src_backward) = bi_lstm_encoder(input_seq=src_embedding, hidden_size=encoder_size)
    src_forward_last = fluid.layers.sequence_last_step(input=src_forward)
    src_backward_first = fluid.layers.sequence_first_step(input=src_backward)
    encoded_vector = fluid.layers.concat(input=[src_forward_last, src_backward_first], axis=1)
    decoder_boot = fluid.layers.fc(input=encoded_vector, size=decoder_size, bias_attr=False, act='tanh')
    trg_word_idx = fluid.layers.data(name='target_sequence', shape=[1], dtype='int64', lod_level=1)
    trg_embedding = fluid.layers.embedding(input=trg_word_idx, size=[target_dict_dim, embedding_dim], dtype='float32')
    prediction = lstm_decoder_without_attention(trg_embedding, decoder_boot, encoded_vector, decoder_size)
    label = fluid.layers.data(name='label_sequence', shape=[1], dtype='int64', lod_level=1)
    cost = fluid.layers.cross_entropy(input=prediction, label=label)
    avg_cost = fluid.layers.mean(x=cost)
    return avg_cost