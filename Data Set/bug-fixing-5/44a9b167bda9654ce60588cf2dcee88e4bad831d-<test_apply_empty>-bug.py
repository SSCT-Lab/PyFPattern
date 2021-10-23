def test_apply_empty(self):
    applied = self.empty.apply(np.sqrt)
    assert applied.empty
    applied = self.empty.apply(np.mean)
    assert applied.empty
    no_rows = self.frame[:0]
    result = no_rows.apply((lambda x: x.mean()))
    expected = Series(np.nan, index=self.frame.columns)
    assert_series_equal(result, expected)
    no_cols = self.frame.loc[:, []]
    result = no_cols.apply((lambda x: x.mean()), axis=1)
    expected = Series(np.nan, index=self.frame.index)
    assert_series_equal(result, expected)
    xp = DataFrame(index=['a'])
    rs = xp.apply((lambda x: x['a']), axis=1)
    assert_frame_equal(xp, rs)