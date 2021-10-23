@keras_test
@pytest.mark.skipif((keras.backend.backend() != 'tensorflow'), reason='Requires TensorFlow backend')
@pytest.mark.skipif((not keras.backend.tensorflow_backend._get_available_gpus()), reason='Requires GPU')
def test_specify_initial_state_keras_tensor():
    input_size = 10
    timesteps = 6
    units = 2
    num_samples = 32
    for layer_class in [keras.layers.CuDNNGRU, keras.layers.CuDNNLSTM]:
        num_states = (2 if (layer_class is keras.layers.CuDNNLSTM) else 1)
        inputs = keras.Input((timesteps, input_size))
        initial_state = [keras.Input((units,)) for _ in range(num_states)]
        layer = layer_class(units)
        if (len(initial_state) == 1):
            output = layer(inputs, initial_state=initial_state[0])
        else:
            output = layer(inputs, initial_state=initial_state)
        assert (initial_state[0] in layer.inbound_nodes[0].input_tensors)
        model = keras.models.Model(([inputs] + initial_state), output)
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        inputs = np.random.random((num_samples, timesteps, input_size))
        initial_state = [np.random.random((num_samples, units)) for _ in range(num_states)]
        targets = np.random.random((num_samples, units))
        model.fit(([inputs] + initial_state), targets)