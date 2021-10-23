def test_valid(self):
    ts = self.ts.copy()
    ts[::2] = np.NaN
    result = ts.dropna()
    assert (len(result) == ts.count())
    tm.assert_series_equal(result, ts[1::2])
    tm.assert_series_equal(result, ts[pd.notna(ts)])