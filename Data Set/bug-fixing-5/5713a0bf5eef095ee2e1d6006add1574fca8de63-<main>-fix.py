def main():
    rnn_out = encoder_decoder()
    label = layers.data(name='target_language_next_word', shape=[1], dtype='int64', lod_level=1)
    cost = layers.cross_entropy(input=rnn_out, label=label)
    avg_cost = fluid.layers.mean(cost)
    optimizer = fluid.optimizer.Adagrad(learning_rate=0.0001)
    optimizer.minimize(avg_cost)
    fluid.release_memory(fluid.default_main_program())
    train_data = paddle.batch(paddle.dataset.wmt14.train(dict_size), batch_size=batch_size)
    place = core.CPUPlace()
    exe = Executor(place)
    exe.run(framework.default_startup_program())
    feed_order = ['src_word_id', 'target_language_word', 'target_language_next_word']
    feed_list = [fluid.default_main_program().global_block().var(var_name) for var_name in feed_order]
    feeder = fluid.DataFeeder(feed_list, place)
    batch_id = 0
    for pass_id in xrange(10):
        for data in train_data():
            outs = exe.run(fluid.default_main_program(), feed=feeder.feed(data), fetch_list=[avg_cost])
            avg_cost_val = np.array(outs[0])
            print(((((('pass_id=' + str(pass_id)) + ' batch=') + str(batch_id)) + ' avg_cost=') + str(avg_cost_val)))
            if (batch_id > 2):
                exit(0)
            if math.isnan(float(avg_cost_val)):
                sys.exit('got NaN loss, training failed.')
            batch_id += 1