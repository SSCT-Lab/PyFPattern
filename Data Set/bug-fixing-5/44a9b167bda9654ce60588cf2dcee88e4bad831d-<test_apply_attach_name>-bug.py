def test_apply_attach_name(self):
    result = self.frame.apply((lambda x: x.name))
    expected = Series(self.frame.columns, index=self.frame.columns)
    assert_series_equal(result, expected)
    result = self.frame.apply((lambda x: x.name), axis=1)
    expected = Series(self.frame.index, index=self.frame.index)
    assert_series_equal(result, expected)
    result = self.frame.apply((lambda x: np.repeat(x.name, len(x))))
    expected = DataFrame(np.tile(self.frame.columns, (len(self.frame.index), 1)), index=self.frame.index, columns=self.frame.columns)
    assert_frame_equal(result, expected)
    result = self.frame.apply((lambda x: np.repeat(x.name, len(x))), axis=1)
    expected = Series((np.repeat(t[0], len(self.frame.columns)) for t in self.frame.itertuples()))
    expected.index = self.frame.index
    assert_series_equal(result, expected)