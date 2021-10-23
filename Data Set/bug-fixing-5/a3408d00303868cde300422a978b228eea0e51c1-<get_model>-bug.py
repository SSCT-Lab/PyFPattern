def get_model(args):
    if args.use_reader_op:
        raise Exception('stacked_dynamic_lstm do not support reader op for now.')
    lstm_size = 512
    emb_dim = 512
    crop_size = 1500
    data = fluid.layers.data(name='words', shape=[1], lod_level=1, dtype='int64')
    sentence = fluid.layers.embedding(input=data, size=[len(word_dict), emb_dim])
    sentence = fluid.layers.fc(input=sentence, size=lstm_size, act='tanh')
    rnn = fluid.layers.DynamicRNN()
    with rnn.block():
        word = rnn.step_input(sentence)
        prev_hidden = rnn.memory(value=0.0, shape=[lstm_size])
        prev_cell = rnn.memory(value=0.0, shape=[lstm_size])

        def gate_common(ipt, hidden, size):
            gate0 = fluid.layers.fc(input=ipt, size=size, bias_attr=True)
            gate1 = fluid.layers.fc(input=hidden, size=size, bias_attr=False)
            gate = fluid.layers.sums(input=[gate0, gate1])
            return gate
        forget_gate = fluid.layers.sigmoid(x=gate_common(word, prev_hidden, lstm_size))
        input_gate = fluid.layers.sigmoid(x=gate_common(word, prev_hidden, lstm_size))
        output_gate = fluid.layers.sigmoid(x=gate_common(word, prev_hidden, lstm_size))
        cell_gate = fluid.layers.tanh(x=gate_common(word, prev_hidden, lstm_size))
        cell = fluid.layers.sums(input=[fluid.layers.elementwise_mul(x=forget_gate, y=prev_cell), fluid.layers.elementwise_mul(x=input_gate, y=cell_gate)])
        hidden = fluid.layers.elementwise_mul(x=output_gate, y=fluid.layers.tanh(x=cell))
        rnn.update_memory(prev_cell, cell)
        rnn.update_memory(prev_hidden, hidden)
        rnn.output(hidden)
    last = fluid.layers.sequence_pool(rnn(), 'last')
    logit = fluid.layers.fc(input=last, size=2, act='softmax')
    loss = fluid.layers.cross_entropy(input=logit, label=fluid.layers.data(name='label', shape=[1], dtype='int64'))
    loss = fluid.layers.mean(x=loss)
    batch_acc = fluid.layers.accuracy(input=logit, label=fluid.layers.data(name='label', shape=[1], dtype='int64'))
    inference_program = fluid.default_main_program().clone()
    with fluid.program_guard(inference_program):
        inference_program = fluid.io.get_inference_program(target_vars=[batch_acc, batch_size_tensor])
    adam = fluid.optimizer.Adam()
    train_reader = batch(paddle.reader.shuffle(crop_sentence(imdb.train(word_dict), crop_size), buf_size=25000), batch_size=(args.batch_size * args.gpus))
    test_reader = batch(paddle.reader.shuffle(crop_sentence(imdb.test(word_dict), crop_size), buf_size=25000), batch_size=args.batch_size)
    return (loss, inference_program, adam, train_reader, test_reader, batch_acc)