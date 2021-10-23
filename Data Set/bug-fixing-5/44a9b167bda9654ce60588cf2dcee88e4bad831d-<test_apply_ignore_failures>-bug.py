def test_apply_ignore_failures(self):
    result = frame_apply(self.mixed_frame, np.mean, 0, ignore_failures=True).apply_standard()
    expected = self.mixed_frame._get_numeric_data().apply(np.mean)
    assert_series_equal(result, expected)