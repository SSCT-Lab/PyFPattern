def test_zero_variance_floating_point_error():
    data = ([[(- 0.13725701)]] * 10)
    if (np.var(data) == 0):
        pytest.skip('This test is not valid for this platform, as it relies on numerical instabilities.')
    for X in [data, csr_matrix(data), csc_matrix(data), bsr_matrix(data)]:
        msg = 'No feature in X meets the variance threshold 0.00000'
        with pytest.raises(ValueError, match=msg):
            VarianceThreshold().fit(X)