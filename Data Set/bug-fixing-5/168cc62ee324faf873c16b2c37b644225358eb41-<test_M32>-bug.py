@XFAIL
def test_M32():
    assert (solve((max((2 - (x ** 2)), x) - max((- x), ((x ** 3) / 9))), assume=Q.real(x)) == [(- 1), 3])