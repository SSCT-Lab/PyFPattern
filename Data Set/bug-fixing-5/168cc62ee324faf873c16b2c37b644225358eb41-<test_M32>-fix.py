@XFAIL
def test_M32():
    assert (solveset_real((Max((2 - (x ** 2)), x) - Max((- x), ((x ** 3) / 9))), x) == FiniteSet((- 1), 3))