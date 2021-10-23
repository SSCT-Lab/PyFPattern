@keras_test
@pytest.mark.skipif((K.backend() != 'tensorflow'), reason='NASNets are supported only on TensorFlow')
def test_nasnet():
    model = applications.NASNetMobile(weights=None)
    assert (model.output_shape == (None, 1000))
    model = applications.NASNetLarge(weights=None)
    assert (model.output_shape == (None, 1000))