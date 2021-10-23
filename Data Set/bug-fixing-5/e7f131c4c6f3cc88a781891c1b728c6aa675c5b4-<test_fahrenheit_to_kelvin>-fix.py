def test_fahrenheit_to_kelvin():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        assert_equal(sc.F2K([32, 32]), [273.15, 273.15])