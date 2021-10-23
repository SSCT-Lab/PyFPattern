def test_long_ar_start_params():
    np.random.seed(12345)
    arparams = np.array([1, (- 0.75), 0.25])
    maparams = np.array([1, 0.65, 0.35])
    nobs = 30
    y = arma_generate_sample(arparams, maparams, nobs)
    model = ARMA(y, order=(2, 2))
    res = model.fit(method='css', start_ar_lags=10, disp=0)
    res = model.fit(method='css-mle', start_ar_lags=10, disp=0)
    res = model.fit(method='mle', start_ar_lags=10, disp=0)
    assert_raises(ValueError, model.fit, start_ar_lags=(nobs + 5), disp=0)