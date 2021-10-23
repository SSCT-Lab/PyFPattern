@XFAIL
def test_M31():
    assert (solve(((1 - abs(x)) - max(((- x) - 2), (x - 2))), x, assume=Q.real(x)) == [((- 3) / 2), (3 / 2)])