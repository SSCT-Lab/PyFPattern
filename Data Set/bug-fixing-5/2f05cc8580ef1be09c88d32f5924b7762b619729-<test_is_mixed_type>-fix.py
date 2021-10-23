def test_is_mixed_type(self, float_frame, float_string_frame):
    assert (not float_frame._is_mixed_type)
    assert float_string_frame._is_mixed_type