def test_cummax(self, datetime_series):
    tm.assert_numpy_array_equal(datetime_series.cummax().values, np.maximum.accumulate(np.array(datetime_series)))
    ts = datetime_series.copy()
    ts[::2] = np.NaN
    result = ts.cummax()[1::2]
    expected = np.maximum.accumulate(ts.dropna())
    tm.assert_series_equal(result, expected)