def test_apply_yield_list(self, float_frame):
    result = float_frame.apply(list)
    assert_frame_equal(result, float_frame)