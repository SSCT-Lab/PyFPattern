def test_corr_callable_method(self, datetime_series):
    my_corr = (lambda a, b: (1.0 if (a == b).all() else 0.0))
    s1 = Series([1, 2, 3, 4, 5])
    s2 = Series([5, 4, 3, 2, 1])
    expected = 0
    tm.assert_almost_equal(s1.corr(s2, method=my_corr), expected)
    tm.assert_almost_equal(datetime_series.corr(datetime_series, method=my_corr), 1.0)
    tm.assert_almost_equal(datetime_series[:15].corr(datetime_series[5:], method=my_corr), 1.0)
    assert np.isnan(datetime_series[::2].corr(datetime_series[1::2], method=my_corr))
    df = pd.DataFrame([s1, s2])
    expected = pd.DataFrame([{
        0: 1.0,
        1: 0,
    }, {
        0: 0,
        1: 1.0,
    }])
    tm.assert_almost_equal(df.transpose().corr(method=my_corr), expected)