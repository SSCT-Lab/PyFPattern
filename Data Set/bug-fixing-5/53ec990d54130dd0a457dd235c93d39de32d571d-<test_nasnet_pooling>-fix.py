@keras_test
@pytest.mark.skipif((K.backend() != 'tensorflow'), reason='NASNets are supported only on TensorFlow')
def test_nasnet_pooling():
    random.seed(time.time())
    (fun, dim) = random.choice(NASNET_LIST)
    model = fun(weights=None, include_top=False, pooling='avg')
    assert (model.output_shape == (None, dim))