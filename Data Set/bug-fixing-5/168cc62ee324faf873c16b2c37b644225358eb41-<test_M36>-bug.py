@XFAIL
def test_M36():
    assert (solve((((f ** 2) + f) - 2), x) == [Eq(f(x), 1), Eq(f(x), (- 2))])