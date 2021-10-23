@keras_test
def test_densenet_no_top():
    random.seed(time.time())
    (fun, dim) = random.choice(DENSENET_LIST)

    def model_fn():
        return fun(weights=None, include_top=False)
    output_shape = clean_run(model_fn)
    assert (output_shape == (None, None, None, dim))