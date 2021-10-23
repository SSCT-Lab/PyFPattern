def test_M36():
    assert (solveset((((f(x) ** 2) + f(x)) - 2), f(x)) == FiniteSet((- 2), 1))