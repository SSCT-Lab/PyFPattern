def test_cast_internals(self):
    casted = DataFrame(self.frame._data, dtype=int)
    expected = DataFrame(self.frame._series, dtype=int)
    assert_frame_equal(casted, expected)
    casted = DataFrame(self.frame._data, dtype=np.int32)
    expected = DataFrame(self.frame._series, dtype=np.int32)
    assert_frame_equal(casted, expected)