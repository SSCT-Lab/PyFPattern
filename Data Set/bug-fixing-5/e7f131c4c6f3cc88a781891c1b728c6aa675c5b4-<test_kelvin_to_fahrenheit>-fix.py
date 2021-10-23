def test_kelvin_to_fahrenheit():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        assert_equal(sc.K2F([273.15, 273.15]), [32, 32])