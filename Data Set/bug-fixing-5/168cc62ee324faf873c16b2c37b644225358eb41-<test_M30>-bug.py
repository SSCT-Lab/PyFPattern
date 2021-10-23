@XFAIL
def test_M30():
    assert (solve((abs(((2 * x) + 5)) - abs((x - 2))), x, assume=Q.real(x)) == [(- 1), (- 7)])