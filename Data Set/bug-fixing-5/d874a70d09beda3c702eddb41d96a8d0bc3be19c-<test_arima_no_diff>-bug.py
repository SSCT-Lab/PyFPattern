def test_arima_no_diff():
    ar = [1, (- 0.75), 0.15, 0.35]
    ma = [1, 0.25, 0.9]
    y = arma_generate_sample(ar, ma, 100)
    mod = ARIMA(y, (3, 0, 2))
    assert_((type(mod) is ARMA))
    res = mod.fit(disp=(- 1))
    res.predict()