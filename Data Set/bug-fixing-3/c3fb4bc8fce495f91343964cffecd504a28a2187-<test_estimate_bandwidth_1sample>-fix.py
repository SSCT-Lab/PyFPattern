def test_estimate_bandwidth_1sample():
    bandwidth = estimate_bandwidth(X, n_samples=1, quantile=0.3)
    assert (bandwidth == pytest.approx(0.0, abs=1e-05))