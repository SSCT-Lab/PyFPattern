def test_arima111_predict_exog_2127():
    ef = [0.03005, 0.03917, 0.02828, 0.03644, 0.03379, 0.02744, 0.03343, 0.02621, 0.0305, 0.02455, 0.03261, 0.03507, 0.02734, 0.05373, 0.02677, 0.03443, 0.03331, 0.02741, 0.03709, 0.02113, 0.03343, 0.02011, 0.03675, 0.03077, 0.02201, 0.04844, 0.05518, 0.03765, 0.05433, 0.03049, 0.04829, 0.02936, 0.04421, 0.02457, 0.04007, 0.03009, 0.04504, 0.05041, 0.03651, 0.02719, 0.04383, 0.02887, 0.0344, 0.03348, 0.02364, 0.03496, 0.02549, 0.03284, 0.03523, 0.02579, 0.0308, 0.01784, 0.03237, 0.02078, 0.03508, 0.03062, 0.02006, 0.02341, 0.02223, 0.03145, 0.03081, 0.0252, 0.02683, 0.0172, 0.02225, 0.01579, 0.02237, 0.02295, 0.0183, 0.02356, 0.02051, 0.02932, 0.03025, 0.0239, 0.02635, 0.01863, 0.02994, 0.01762, 0.02837, 0.02421, 0.01951, 0.02149, 0.02079, 0.02528, 0.02575, 0.01634, 0.02563, 0.01719, 0.02915, 0.01724, 0.02804, 0.0275, 0.02099, 0.02522, 0.02422, 0.03254, 0.02095, 0.03241, 0.01867, 0.03998, 0.02212, 0.03034, 0.03419, 0.01866, 0.02623, 0.02052]
    ue = [4.9, 5.0, 5.0, 5.0, 4.9, 4.7, 4.8, 4.7, 4.7, 4.6, 4.6, 4.7, 4.7, 4.5, 4.4, 4.5, 4.4, 4.6, 4.5, 4.4, 4.5, 4.4, 4.6, 4.7, 4.6, 4.7, 4.7, 4.7, 5.0, 5.0, 4.9, 5.1, 5.0, 5.4, 5.6, 5.8, 6.1, 6.1, 6.5, 6.8, 7.3, 7.8, 8.3, 8.7, 9.0, 9.4, 9.5, 9.5, 9.6, 9.8, 10.0, 9.9, 9.9, 9.7, 9.8, 9.9, 9.9, 9.6, 9.4, 9.5, 9.5, 9.5, 9.5, 9.8, 9.4, 9.1, 9.0, 9.0, 9.1, 9.0, 9.1, 9.0, 9.0, 9.0, 8.8, 8.6, 8.5, 8.2, 8.3, 8.2, 8.2, 8.2, 8.2, 8.2, 8.1, 7.8, 7.8, 7.8, 7.9, 7.9, 7.7, 7.5, 7.5, 7.5, 7.5, 7.3, 7.2, 7.2, 7.2, 7.0, 6.7, 6.6, 6.7, 6.7, 6.3, 6.3]
    ue = (np.array(ue) / 100)
    model = ARIMA(ef, (1, 1, 1), exog=ue)
    res = model.fit(transparams=False, pgtol=1e-08, iprint=0, disp=0)
    assert_equal(res.mle_retvals['warnflag'], 0)
    predicts = res.predict(start=len(ef), end=(len(ef) + 10), exog=ue[(- 11):], typ='levels')
    predicts_res = np.array([0.02591095, 0.02321325, 0.02436579, 0.02368759, 0.02389753, 0.02372, 0.0237481, 0.0236738, 0.023644, 0.0236283, 0.02362267])
    assert_allclose(predicts, predicts_res, atol=5e-06)
    res.forecast(steps=10, exog=np.empty(10))
    with pytest.raises(ValueError):
        res.forecast(steps=10)
    with pytest.raises(ValueError):
        res.forecast(steps=10, exog=np.empty((10, 2)))
    with pytest.raises(ValueError):
        res.forecast(steps=10, exog=np.empty(100))