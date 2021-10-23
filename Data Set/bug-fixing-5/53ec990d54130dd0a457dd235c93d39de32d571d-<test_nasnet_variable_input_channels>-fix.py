@keras_test
@pytest.mark.skipif((K.backend() != 'tensorflow'), reason='NASNets are supported only on TensorFlow')
def test_nasnet_variable_input_channels():
    random.seed(time.time())
    (fun, dim) = random.choice(NASNET_LIST)
    input_shape = ((1, None, None) if (K.image_data_format() == 'channels_first') else (None, None, 1))
    model = fun(weights=None, include_top=False, input_shape=input_shape)
    assert (model.output_shape == (None, None, None, dim))
    input_shape = ((4, None, None) if (K.image_data_format() == 'channels_first') else (None, None, 4))
    model = fun(weights=None, include_top=False, input_shape=input_shape)
    assert (model.output_shape == (None, None, None, dim))