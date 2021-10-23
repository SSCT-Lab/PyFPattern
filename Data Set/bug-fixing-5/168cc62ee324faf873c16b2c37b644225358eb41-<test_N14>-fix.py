@XFAIL
def test_N14():
    x = Symbol('x')
    assert (solveset((sin(x) < 1), x, domain=S.Reals) == Union(Interval((- oo), (pi / 2), True, True), Interval((pi / 2), oo, True, True)))