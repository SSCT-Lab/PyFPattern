

def test_qz_single(self):
    n = 5
    A = random([n, n]).astype(float32)
    B = random([n, n]).astype(float32)
    (AA, BB, Q, Z) = qz(A, B)
    assert_array_almost_equal(dot(dot(Q, AA), Z.T), A)
    assert_array_almost_equal(dot(dot(Q, BB), Z.T), B)
    assert_array_almost_equal(dot(Q, Q.T), eye(n))
    assert_array_almost_equal(dot(Z, Z.T), eye(n))
    assert_(all((diag(BB) >= 0)))
