def test_estimate_bandwidth_1sample():
    bandwidth = estimate_bandwidth(X, n_samples=1, quantile=0.3)
    assert_array_almost_equal(bandwidth, 0.0, decimal=5)