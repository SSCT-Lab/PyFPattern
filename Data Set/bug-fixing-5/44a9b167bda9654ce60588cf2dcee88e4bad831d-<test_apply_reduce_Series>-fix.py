def test_apply_reduce_Series(self, float_frame):
    float_frame.loc[::2, 'A'] = np.nan
    expected = float_frame.mean(1)
    result = float_frame.apply(np.mean, axis=1)
    assert_series_equal(result, expected)