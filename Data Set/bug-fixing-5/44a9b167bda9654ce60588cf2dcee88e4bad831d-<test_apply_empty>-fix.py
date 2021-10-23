def test_apply_empty(self, float_frame, empty_frame):
    applied = empty_frame.apply(np.sqrt)
    assert applied.empty
    applied = empty_frame.apply(np.mean)
    assert applied.empty
    no_rows = float_frame[:0]
    result = no_rows.apply((lambda x: x.mean()))
    expected = Series(np.nan, index=float_frame.columns)
    assert_series_equal(result, expected)
    no_cols = float_frame.loc[:, []]
    result = no_cols.apply((lambda x: x.mean()), axis=1)
    expected = Series(np.nan, index=float_frame.index)
    assert_series_equal(result, expected)
    xp = DataFrame(index=['a'])
    rs = xp.apply((lambda x: x['a']), axis=1)
    assert_frame_equal(xp, rs)