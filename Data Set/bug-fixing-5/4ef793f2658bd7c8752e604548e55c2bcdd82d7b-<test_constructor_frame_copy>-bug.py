def test_constructor_frame_copy(self):
    cop = DataFrame(self.frame, copy=True)
    cop['A'] = 5
    assert (cop['A'] == 5).all()
    assert (not (self.frame['A'] == 5).all())