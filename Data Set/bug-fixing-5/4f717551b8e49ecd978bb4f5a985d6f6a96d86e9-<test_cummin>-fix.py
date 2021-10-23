def test_cummin(self, datetime_series):
    tm.assert_numpy_array_equal(datetime_series.cummin().values, np.minimum.accumulate(np.array(datetime_series)))
    ts = datetime_series.copy()
    ts[::2] = np.NaN
    result = ts.cummin()[1::2]
    expected = np.minimum.accumulate(ts.dropna())
    tm.assert_series_equal(result, expected)