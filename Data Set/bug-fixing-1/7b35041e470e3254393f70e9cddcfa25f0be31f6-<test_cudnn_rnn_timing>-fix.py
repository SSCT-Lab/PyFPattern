

@keras_test
@pytest.mark.parametrize('rnn_type', ['lstm', 'gru'], ids=['LSTM', 'GRU'])
@pytest.mark.skipif((keras.backend.backend() != 'tensorflow'), reason='Requires TensorFlow backend')
@pytest.mark.skipif((not keras.backend.tensorflow_backend._get_available_gpus()), reason='Requires GPU')
def test_cudnn_rnn_timing(rnn_type):
    input_size = 1000
    timesteps = 60
    units = 256
    num_samples = 10000
    times = []
    for use_cudnn in [True, False]:
        start_time = time.time()
        inputs = keras.layers.Input(shape=(None, input_size))
        if use_cudnn:
            if (rnn_type == 'lstm'):
                layer = keras.layers.CuDNNLSTM(units)
            else:
                layer = keras.layers.CuDNNGRU(units)
        elif (rnn_type == 'lstm'):
            layer = keras.layers.LSTM(units)
        else:
            layer = keras.layers.GRU(units)
        outputs = layer(inputs)
        model = keras.models.Model(inputs, outputs)
        model.compile('sgd', 'mse')
        x = np.random.random((num_samples, timesteps, input_size))
        y = np.random.random((num_samples, units))
        model.fit(x, y, epochs=4, batch_size=32)
        times.append((time.time() - start_time))
    speedup = (times[1] / times[0])
    print(rnn_type, 'speedup', speedup)
    assert (speedup > 3)
