def layer_test(layer_cls, kwargs=None, input_shape=None, input_dtype=None, input_data=None, expected_output=None, expected_output_dtype=None):
    'Test routine for a layer with a single input and single output.\n\n  Arguments:\n    layer_cls: Layer class object.\n    kwargs: Optional dictionary of keyword arguments for instantiating the\n      layer.\n    input_shape: Input shape tuple.\n    input_dtype: Data type of the input data.\n    input_data: Numpy array of input data.\n    expected_output: Shape tuple for the expected shape of the output.\n    expected_output_dtype: Data type expected for the output.\n\n  Returns:\n    The output data (Numpy array) returned by the layer, for additional\n    checks to be done by the calling code.\n  '
    if (input_data is None):
        assert input_shape
        if (not input_dtype):
            input_dtype = 'float32'
        input_data_shape = list(input_shape)
        for (i, e) in enumerate(input_data_shape):
            if (e is None):
                input_data_shape[i] = np.random.randint(1, 4)
        input_data = (10 * np.random.random(input_data_shape))
        if (input_dtype[:5] == 'float'):
            input_data -= 0.5
        input_data = input_data.astype(input_dtype)
    elif (input_shape is None):
        input_shape = input_data.shape
    if (input_dtype is None):
        input_dtype = input_data.dtype
    if (expected_output_dtype is None):
        expected_output_dtype = input_dtype
    kwargs = (kwargs or {
        
    })
    layer = layer_cls(**kwargs)
    weights = layer.get_weights()
    layer.set_weights(weights)
    if ('weights' in tf_inspect.getargspec(layer_cls.__init__)):
        kwargs['weights'] = weights
        layer = layer_cls(**kwargs)
    x = keras.layers.Input(shape=input_shape[1:], dtype=input_dtype)
    y = layer(x)
    assert (keras.backend.dtype(y) == expected_output_dtype)
    model = keras.models.Model(x, y)
    expected_output_shape = tuple(layer._compute_output_shape(input_shape).as_list())
    actual_output = model.predict(input_data)
    actual_output_shape = actual_output.shape
    for (expected_dim, actual_dim) in zip(expected_output_shape, actual_output_shape):
        if (expected_dim is not None):
            assert (expected_dim == actual_dim)
    if (expected_output is not None):
        np.testing.assert_allclose(actual_output, expected_output, rtol=0.001)
    model_config = model.get_config()
    recovered_model = keras.models.Model.from_config(model_config)
    if model.weights:
        weights = model.get_weights()
        recovered_model.set_weights(weights)
        output = recovered_model.predict(input_data)
        np.testing.assert_allclose(output, actual_output, rtol=0.001)
    model.compile('rmsprop', 'mse')
    model.train_on_batch(input_data, actual_output)
    layer_config = layer.get_config()
    layer_config['batch_input_shape'] = input_shape
    layer = layer.__class__.from_config(layer_config)
    model = keras.models.Sequential()
    model.add(layer)
    actual_output = model.predict(input_data)
    actual_output_shape = actual_output.shape
    for (expected_dim, actual_dim) in zip(expected_output_shape, actual_output_shape):
        if (expected_dim is not None):
            assert (expected_dim == actual_dim)
    if (expected_output is not None):
        np.testing.assert_allclose(actual_output, expected_output, rtol=0.001)
    model_config = model.get_config()
    recovered_model = keras.models.Sequential.from_config(model_config)
    if model.weights:
        weights = model.get_weights()
        recovered_model.set_weights(weights)
        output = recovered_model.predict(input_data)
        np.testing.assert_allclose(output, actual_output, rtol=0.001)
    model.compile('rmsprop', 'mse')
    model.train_on_batch(input_data, actual_output)
    return actual_output