@keras_test
@pytest.mark.parametrize('fun', [applications.DenseNet121, applications.DenseNet169, applications.DenseNet201], ids=['DenseNet121', 'DenseNet169', 'DenseNet201'])
def test_densenet(fun):

    def model_fn():
        return fun(weights=None)
    output_shape = clean_run(model_fn)
    assert (output_shape == (None, 1000))