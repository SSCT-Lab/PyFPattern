@keras_test
@pytest.mark.skipif((K.backend() != 'tensorflow'), reason='NASNets are supported only on TensorFlow')
def test_nasnet_pooling():
    model = applications.NASNetMobile(weights=None, include_top=False, pooling='avg')
    assert (model.output_shape == (None, 1056))
    model = applications.NASNetLarge(weights=None, include_top=False, pooling='avg')
    assert (model.output_shape == (None, 4032))