def test_apply_reduce_Series(self):
    self.frame.loc[::2, 'A'] = np.nan
    expected = self.frame.mean(1)
    result = self.frame.apply(np.mean, axis=1)
    assert_series_equal(result, expected)