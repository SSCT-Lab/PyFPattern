def test_interpolate(self):
    ts = Series(np.arange(len(self.ts), dtype=float), self.ts.index)
    ts_copy = ts.copy()
    ts_copy[5:10] = np.NaN
    linear_interp = ts_copy.interpolate(method='linear')
    tm.assert_series_equal(linear_interp, ts)
    ord_ts = Series([d.toordinal() for d in self.ts.index], index=self.ts.index).astype(float)
    ord_ts_copy = ord_ts.copy()
    ord_ts_copy[5:10] = np.NaN
    time_interp = ord_ts_copy.interpolate(method='time')
    tm.assert_series_equal(time_interp, ord_ts)
    non_ts = self.series.copy()
    non_ts[0] = np.NaN
    pytest.raises(ValueError, non_ts.interpolate, method='time')