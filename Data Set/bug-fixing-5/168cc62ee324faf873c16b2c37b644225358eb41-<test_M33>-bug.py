@XFAIL
def test_M33():
    assert (solve((max((2 - (x ** 2)), x) - ((x ** 3) / 9)), assume=Q.real(x)) == [(- 3), (- 1.554894), 3])