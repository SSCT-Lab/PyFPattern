def test_apply_yield_list(self):
    result = self.frame.apply(list)
    assert_frame_equal(result, self.frame)