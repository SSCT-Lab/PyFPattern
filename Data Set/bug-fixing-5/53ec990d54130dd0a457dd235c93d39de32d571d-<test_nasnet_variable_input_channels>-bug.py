@keras_test
@pytest.mark.skipif((K.backend() != 'tensorflow'), reason='NASNets are supported only on TensorFlow')
def test_nasnet_variable_input_channels():
    input_shape = ((1, None, None) if (K.image_data_format() == 'channels_first') else (None, None, 1))
    model = applications.NASNetMobile(weights=None, include_top=False, input_shape=input_shape)
    assert (model.output_shape == (None, None, None, 1056))
    model = applications.NASNetLarge(weights=None, include_top=False, input_shape=input_shape)
    assert (model.output_shape == (None, None, None, 4032))
    input_shape = ((4, None, None) if (K.image_data_format() == 'channels_first') else (None, None, 4))
    model = applications.NASNetMobile(weights=None, include_top=False, input_shape=input_shape)
    assert (model.output_shape == (None, None, None, 1056))
    model = applications.NASNetLarge(weights=None, include_top=False, input_shape=input_shape)
    assert (model.output_shape == (None, None, None, 4032))