def test_P37():
    M = Matrix([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
    assert ((M ** Rational(1, 2)) == Matrix([[1, R(1, 2), 0], [0, 1, 0], [0, 0, 1]]))