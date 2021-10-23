@XFAIL
def test_U4():
    n = symbols('n', integer=True, positive=True)
    x = symbols('x', real=True)
    d = diff((x ** n), x, n)
    assert (d.rewrite(factorial) == factorial(n))