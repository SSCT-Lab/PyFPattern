@keras_test
def test_densenet():
    random.seed(time.time())
    (fun, _) = random.choice(DENSENET_LIST)

    def model_fn():
        return fun(weights=None)
    output_shape = clean_run(model_fn)
    assert (output_shape == (None, 1000))