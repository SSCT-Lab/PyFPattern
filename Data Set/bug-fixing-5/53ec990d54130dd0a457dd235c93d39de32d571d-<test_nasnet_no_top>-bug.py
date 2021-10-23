@keras_test
@pytest.mark.skipif((K.backend() != 'tensorflow'), reason='NASNets are supported only on TensorFlow')
def test_nasnet_no_top():
    model = applications.NASNetMobile(weights=None, include_top=False)
    assert (model.output_shape == (None, None, None, 1056))
    model = applications.NASNetLarge(weights=None, include_top=False)
    assert (model.output_shape == (None, None, None, 4032))