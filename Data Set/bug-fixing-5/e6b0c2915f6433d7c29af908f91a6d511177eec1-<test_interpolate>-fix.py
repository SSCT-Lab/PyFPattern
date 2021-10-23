def test_interpolate(self, datetime_series, string_series):
    ts = Series(np.arange(len(datetime_series), dtype=float), datetime_series.index)
    ts_copy = ts.copy()
    ts_copy[5:10] = np.NaN
    linear_interp = ts_copy.interpolate(method='linear')
    tm.assert_series_equal(linear_interp, ts)
    ord_ts = Series([d.toordinal() for d in datetime_series.index], index=datetime_series.index).astype(float)
    ord_ts_copy = ord_ts.copy()
    ord_ts_copy[5:10] = np.NaN
    time_interp = ord_ts_copy.interpolate(method='time')
    tm.assert_series_equal(time_interp, ord_ts)
    non_ts = string_series.copy()
    non_ts[0] = np.NaN
    pytest.raises(ValueError, non_ts.interpolate, method='time')