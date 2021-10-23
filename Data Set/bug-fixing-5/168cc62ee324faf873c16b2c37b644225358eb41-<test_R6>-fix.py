def test_R6():
    (n, k) = symbols('n k', integer=True, positive=True)
    gn = MatrixSymbol('gn', (n + 2), 1)
    Sm = Sum((gn[(k, 0)] - gn[((k - 1), 0)]), (k, 1, (n + 1)))
    assert (Sm.doit() == ((- gn[(0, 0)]) + gn[((n + 1), 0)]))