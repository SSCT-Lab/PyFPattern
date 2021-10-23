def test_apply_ignore_failures(self, float_string_frame):
    result = frame_apply(float_string_frame, np.mean, 0, ignore_failures=True).apply_standard()
    expected = float_string_frame._get_numeric_data().apply(np.mean)
    assert_series_equal(result, expected)