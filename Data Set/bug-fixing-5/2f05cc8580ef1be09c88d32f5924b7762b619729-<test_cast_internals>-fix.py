def test_cast_internals(self, float_frame):
    casted = DataFrame(float_frame._data, dtype=int)
    expected = DataFrame(float_frame._series, dtype=int)
    assert_frame_equal(casted, expected)
    casted = DataFrame(float_frame._data, dtype=np.int32)
    expected = DataFrame(float_frame._series, dtype=np.int32)
    assert_frame_equal(casted, expected)