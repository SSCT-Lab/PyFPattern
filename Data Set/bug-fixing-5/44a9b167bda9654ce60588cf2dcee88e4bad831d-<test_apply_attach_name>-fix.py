def test_apply_attach_name(self, float_frame):
    result = float_frame.apply((lambda x: x.name))
    expected = Series(float_frame.columns, index=float_frame.columns)
    assert_series_equal(result, expected)
    result = float_frame.apply((lambda x: x.name), axis=1)
    expected = Series(float_frame.index, index=float_frame.index)
    assert_series_equal(result, expected)
    result = float_frame.apply((lambda x: np.repeat(x.name, len(x))))
    expected = DataFrame(np.tile(float_frame.columns, (len(float_frame.index), 1)), index=float_frame.index, columns=float_frame.columns)
    assert_frame_equal(result, expected)
    result = float_frame.apply((lambda x: np.repeat(x.name, len(x))), axis=1)
    expected = Series((np.repeat(t[0], len(float_frame.columns)) for t in float_frame.itertuples()))
    expected.index = float_frame.index
    assert_series_equal(result, expected)