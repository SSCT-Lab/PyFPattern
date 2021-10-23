@XFAIL
def test_R1():
    (i, n) = symbols('i n', integer=True, positive=True)
    xn = MatrixSymbol('xn', n, 1)
    Sm = Sum(((xn[(i, 0)] - (Sum(xn[(j, 0)], (j, 0, (n - 1))) / n)) ** 2), (i, 0, (n - 1)))
    Sm.doit()