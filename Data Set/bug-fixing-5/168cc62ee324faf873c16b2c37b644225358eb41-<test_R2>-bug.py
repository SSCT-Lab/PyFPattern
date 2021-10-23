@XFAIL
def test_R2():
    (m, b) = symbols('m b')
    (i, n) = symbols('i n', integer=True, positive=True)
    xn = MatrixSymbol('xn', n, 1)
    yn = MatrixSymbol('yn', n, 1)
    f = Sum((((yn[(i, 0)] - (m * xn[(i, 0)])) - b) ** 2), (i, 0, (n - 1)))
    f1 = diff(f, m)
    f2 = diff(f, b)
    solveset((f1, f2), m, b, domain=S.Reals)