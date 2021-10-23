def test_cummax(self):
    tm.assert_numpy_array_equal(self.ts.cummax().values, np.maximum.accumulate(np.array(self.ts)))
    ts = self.ts.copy()
    ts[::2] = np.NaN
    result = ts.cummax()[1::2]
    expected = np.maximum.accumulate(ts.dropna())
    tm.assert_series_equal(result, expected)