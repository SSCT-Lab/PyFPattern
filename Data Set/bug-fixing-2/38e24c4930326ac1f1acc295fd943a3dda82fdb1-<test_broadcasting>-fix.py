

def test_broadcasting(self):
    np.random.seed(1234)
    n = 4
    data = np.random.randn(n, n)
    cov = np.dot(data, data.T)
    mean = np.random.randn(n)
    X = np.random.randn(2, 3, n)
    desired_pdf = multivariate_normal.pdf(X, mean, cov)
    desired_cdf = multivariate_normal.cdf(X, mean, cov)
    for i in range(2):
        for j in range(3):
            actual = multivariate_normal.pdf(X[(i, j)], mean, cov)
            assert_allclose(actual, desired_pdf[(i, j)])
            actual = multivariate_normal.cdf(X[(i, j)], mean, cov)
            assert_allclose(actual, desired_cdf[(i, j)], rtol=0.001)
