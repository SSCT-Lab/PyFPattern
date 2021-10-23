@keras_test
@pytest.mark.parametrize('fun,dim', [(applications.DenseNet121, 1024), (applications.DenseNet169, 1664), (applications.DenseNet201, 1920)], ids=['DenseNet121', 'DenseNet169', 'DenseNet201'])
def test_densenet_pooling(fun, dim):

    def model_fn():
        return fun(weights=None, include_top=False, pooling='avg')
    output_shape = clean_run(model_fn)
    assert (output_shape == (None, None, None, dim))