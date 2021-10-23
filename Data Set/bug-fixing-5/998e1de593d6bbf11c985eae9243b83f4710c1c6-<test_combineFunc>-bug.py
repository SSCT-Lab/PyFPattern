def test_combineFunc(self):
    result = (self.frame * 2)
    tm.assert_numpy_array_equal(result.values, (self.frame.values * 2))
    result = (self.mixed_float * 2)
    for (c, s) in compat.iteritems(result):
        tm.assert_numpy_array_equal(s.values, (self.mixed_float[c].values * 2))
    _check_mixed_float(result, dtype=dict(C=None))
    result = (self.empty * 2)
    assert (result.index is self.empty.index)
    assert (len(result.columns) == 0)