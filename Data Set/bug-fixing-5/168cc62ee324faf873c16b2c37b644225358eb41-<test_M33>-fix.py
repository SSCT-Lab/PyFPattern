@XFAIL
def test_M33():
    assert (solveset_real((Max((2 - (x ** 2)), x) - ((x ** 3) / 9)), x) == FiniteSet((- 3), (- 1.554894), 3))