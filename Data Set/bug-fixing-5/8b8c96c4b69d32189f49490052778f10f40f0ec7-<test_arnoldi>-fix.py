def test_arnoldi(self):
    np.random.rand(1234)
    A = (eye(2000) + rand(2000, 2000, density=0.0005))
    b = np.random.rand(2000)
    with suppress_warnings() as sup:
        sup.filter(DeprecationWarning, '.*called without specifying.*')
        (x0, flag0) = gcrotmk(A, b, x0=zeros(A.shape[0]), m=15, k=0, maxiter=1)
        (x1, flag1) = gmres(A, b, x0=zeros(A.shape[0]), restart=15, maxiter=1)
    assert_equal(flag0, 1)
    assert_equal(flag1, 1)
    assert_((np.linalg.norm((A.dot(x0) - b)) > 0.001))
    assert_allclose(x0, x1)