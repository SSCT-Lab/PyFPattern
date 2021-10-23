def test_celcius_to_fahrenheit():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        assert_equal(sc.C2F([0, 0]), [32, 32])