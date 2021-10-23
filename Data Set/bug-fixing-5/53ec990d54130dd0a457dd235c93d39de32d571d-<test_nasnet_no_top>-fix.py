@keras_test
@pytest.mark.skipif((K.backend() != 'tensorflow'), reason='NASNets are supported only on TensorFlow')
def test_nasnet_no_top():
    random.seed(time.time())
    (fun, dim) = random.choice(NASNET_LIST)
    model = fun(weights=None, include_top=False)
    assert (model.output_shape == (None, None, None, dim))