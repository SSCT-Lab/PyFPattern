@pytest.mark.parametrize('dm', [1, 2])
def test_corr_nearest_factor_sparse(self, dm):
    d = 100
    X = np.zeros((d, dm), dtype=np.float64)
    x = np.linspace(0, (2 * np.pi), d)
    np.random.seed(10)
    for j in range(dm):
        X[:, j] = (np.sin((x * (j + 1))) + (1e-10 * np.random.randn(d)))
    _project_correlation_factors(X)
    X *= 0.7
    mat = np.dot(X, X.T)
    np.fill_diagonal(mat, 1)
    mat *= (np.abs(mat) >= 0.35)
    smat = sparse.csr_matrix(mat)
    try:
        rslt = corr_nearest_factor(mat, dm, maxiter=10000)
        assert (rslt.Converged is True)
        mat_dense = rslt.corr.to_matrix()
        rslt = corr_nearest_factor(smat, dm, maxiter=10000)
        assert (rslt.Converged is True)
        mat_sparse = rslt.corr.to_matrix()
        assert_allclose(mat_dense, mat_sparse, rtol=0.25, atol=0.001)
    except AssertionError as err:
        if PLATFORM_WIN32:
            pytest.xfail('Known to randomly fail on Win32')
        raise err