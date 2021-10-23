@keras_test
@pytest.mark.skipif((K.backend() != 'tensorflow'), reason='NASNets are supported only on TensorFlow')
def test_nasnet():
    random.seed(time.time())
    (fun, _) = random.choice(NASNET_LIST)
    model = fun(weights=None)
    assert (model.output_shape == (None, 1000))