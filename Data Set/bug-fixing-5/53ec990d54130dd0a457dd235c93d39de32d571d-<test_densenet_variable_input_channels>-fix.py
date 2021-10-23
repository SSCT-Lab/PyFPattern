@keras_test
def test_densenet_variable_input_channels():
    random.seed(time.time())
    (fun, dim) = random.choice(DENSENET_LIST)

    def model_fn(input_shape):
        return fun(weights=None, include_top=False, input_shape=input_shape)
    output_shape = clean_run((lambda : model_fn((None, None, 1))))
    assert (output_shape == (None, None, None, dim))
    output_shape = clean_run((lambda : model_fn((None, None, 4))))
    assert (output_shape == (None, None, None, dim))