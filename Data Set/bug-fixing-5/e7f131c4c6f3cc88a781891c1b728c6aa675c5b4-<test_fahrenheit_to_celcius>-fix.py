def test_fahrenheit_to_celcius():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        assert_equal(sc.F2C(32), 0)
        assert_equal(sc.F2C([32, 32]), [0, 0])