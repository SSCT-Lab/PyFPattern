def test_fahrenheit_to_celcius():
    assert_equal(sc.F2C(32), 0)
    assert_equal(sc.F2C([32, 32]), [0, 0])