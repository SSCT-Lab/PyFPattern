def test_celcius_to_kelvin():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        assert_equal(sc.C2K([0, 0]), [273.15, 273.15])