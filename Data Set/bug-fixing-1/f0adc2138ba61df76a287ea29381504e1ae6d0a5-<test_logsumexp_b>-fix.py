

def test_logsumexp_b():
    a = np.arange(200)
    b = np.arange(200, 0, (- 1))
    desired = np.log(np.sum((b * np.exp(a))))
    assert_almost_equal(logsumexp(a, b=b), desired)
    a = [1000, 1000]
    b = [1.2, 1.2]
    desired = (1000 + np.log((2 * 1.2)))
    assert_almost_equal(logsumexp(a, b=b), desired)
    x = np.array(([1e-40] * 100000))
    b = np.linspace(1, 1000, 100000)
    logx = np.log(x)
    X = np.vstack((x, x))
    logX = np.vstack((logx, logx))
    B = np.vstack((b, b))
    assert_array_almost_equal(np.exp(logsumexp(logX, b=B)), (B * X).sum())
    assert_array_almost_equal(np.exp(logsumexp(logX, b=B, axis=0)), (B * X).sum(axis=0))
    assert_array_almost_equal(np.exp(logsumexp(logX, b=B, axis=1)), (B * X).sum(axis=1))
