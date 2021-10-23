def test_boolean_set_uncons(self, float_frame):
    float_frame['E'] = 7.0
    expected = float_frame.values.copy()
    expected[(expected > 1)] = 2
    float_frame[(float_frame > 1)] = 2
    assert_almost_equal(expected, float_frame.values)