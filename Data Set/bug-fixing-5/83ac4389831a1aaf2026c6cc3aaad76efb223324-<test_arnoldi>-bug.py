@pytest.mark.skipif((python_implementation() == 'PyPy'), reason='Fails on PyPy CI runs. See #9507')
def test_arnoldi(self):
    np.random.rand(1234)
    A = (eye(10000) + rand(10000, 10000, density=0.0001))
    b = np.random.rand(10000)
    with suppress_warnings() as sup:
        sup.filter(DeprecationWarning, '.*called without specifying.*')
        (x0, flag0) = lgmres(A, b, x0=zeros(A.shape[0]), inner_m=15, maxiter=1)
        (x1, flag1) = gmres(A, b, x0=zeros(A.shape[0]), restart=15, maxiter=1)
    assert_equal(flag0, 1)
    assert_equal(flag1, 1)
    assert_((np.linalg.norm((A.dot(x0) - b)) > 0.001))
    assert_allclose(x0, x1)