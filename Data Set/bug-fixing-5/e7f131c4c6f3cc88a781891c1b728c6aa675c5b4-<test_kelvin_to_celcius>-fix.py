def test_kelvin_to_celcius():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        assert_equal(sc.K2C([0, 0]), [(- 273.15), (- 273.15)])