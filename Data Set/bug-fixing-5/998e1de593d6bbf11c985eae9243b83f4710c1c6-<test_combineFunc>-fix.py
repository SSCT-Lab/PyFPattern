def test_combineFunc(self, float_frame, mixed_float_frame):
    result = (float_frame * 2)
    tm.assert_numpy_array_equal(result.values, (float_frame.values * 2))
    result = (mixed_float_frame * 2)
    for (c, s) in compat.iteritems(result):
        tm.assert_numpy_array_equal(s.values, (mixed_float_frame[c].values * 2))
    _check_mixed_float(result, dtype=dict(C=None))
    result = (DataFrame() * 2)
    assert result.index.equals(DataFrame().index)
    assert (len(result.columns) == 0)