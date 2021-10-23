def test_M31():
    assert (solveset_real(((1 - abs(x)) - Max(((- x) - 2), (x - 2))), x) == FiniteSet(((- S(3)) / 2), (S(3) / 2)))