def test_is_mixed_type(self):
    assert (not self.frame._is_mixed_type)
    assert self.mixed_frame._is_mixed_type