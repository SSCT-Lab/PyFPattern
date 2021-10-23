def test_constructor_frame_copy(self, float_frame):
    cop = DataFrame(float_frame, copy=True)
    cop['A'] = 5
    assert (cop['A'] == 5).all()
    assert (not (float_frame['A'] == 5).all())