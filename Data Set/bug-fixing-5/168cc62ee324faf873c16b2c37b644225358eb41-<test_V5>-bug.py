@XFAIL
def test_V5():
    assert (integrate(((((3 * x) - 5) ** 2) / (((2 * x) - 1) ** Rational(7, 2))), x) == ((((- 41) + (80 * x)) - (45 * (x ** 2))) / (5 * (((2 * x) - 1) ** Rational(5, 2)))))