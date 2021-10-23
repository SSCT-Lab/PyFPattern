@keras_test
@pytest.mark.parametrize('fun,dim', [(applications.DenseNet121, 1024), (applications.DenseNet169, 1664), (applications.DenseNet201, 1920)], ids=['DenseNet121', 'DenseNet169', 'DenseNet201'])
def test_densenet_variable_input_channels(fun, dim):

    def model_fn(input_shape):
        return fun(weights=None, include_top=False, input_shape=input_shape)
    output_shape = clean_run((lambda : model_fn((None, None, 1))))
    assert (output_shape == (None, None, None, dim))
    output_shape = clean_run((lambda : model_fn((None, None, 4))))
    assert (output_shape == (None, None, None, dim))