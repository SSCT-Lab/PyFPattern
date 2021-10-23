def test_cummin(self):
    tm.assert_numpy_array_equal(self.ts.cummin().values, np.minimum.accumulate(np.array(self.ts)))
    ts = self.ts.copy()
    ts[::2] = np.NaN
    result = ts.cummin()[1::2]
    expected = np.minimum.accumulate(ts.dropna())
    tm.assert_series_equal(result, expected)