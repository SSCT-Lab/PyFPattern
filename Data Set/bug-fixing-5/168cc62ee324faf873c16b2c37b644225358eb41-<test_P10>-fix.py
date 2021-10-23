@XFAIL
def test_P10():
    M = Matrix([[1, (2 + (3 * I))], [f((4 - (5 * I))), 6]])
    assert (M.H == Matrix([[1, f((4 + (5 * I)))], [(2 + (3 * I)), 6]]))