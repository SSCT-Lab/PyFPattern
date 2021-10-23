@XFAIL
def test_U4():
    n = symbols('n', integer=True, positive=True)
    x = symbols('x', real=True)
    diff((x ** n), x, n)
    assert (diff((x ** n), x, n).rewrite(factorial) == factorial(n))