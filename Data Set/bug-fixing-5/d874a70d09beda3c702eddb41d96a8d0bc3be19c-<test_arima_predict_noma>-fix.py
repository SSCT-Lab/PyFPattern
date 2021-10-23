def test_arima_predict_noma():
    ar = [1, 0.75]
    ma = [1]
    np.random.seed(12345)
    data = arma_generate_sample(ar, ma, 100)
    arma = ARMA(data, order=(0, 1))
    arma_res = arma.fit(disp=(- 1))
    arma_res.forecast(1)