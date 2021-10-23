def test_broadcasting(self):
    np.random.seed(1234)
    n = 4
    data = np.random.randn(n, n)
    cov = np.dot(data, data.T)
    mean = np.random.randn(n)
    X = np.random.randn(2, 3, n)
    for i in range(2):
        for j in range(3):
            actual = multivariate_normal.pdf(X[(i, j)], mean, cov)
            desired = multivariate_normal.pdf(X, mean, cov)[(i, j)]
            assert_allclose(actual, desired)
            actual = multivariate_normal.cdf(X[(i, j)], mean, cov)
            desired = multivariate_normal.cdf(X, mean, cov)[(i, j)]
            assert_allclose(actual, desired, atol=1e-05)