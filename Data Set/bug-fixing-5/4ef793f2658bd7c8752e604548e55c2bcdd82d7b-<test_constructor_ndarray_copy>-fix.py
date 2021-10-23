def test_constructor_ndarray_copy(self, float_frame):
    df = DataFrame(float_frame.values)
    float_frame.values[5] = 5
    assert (df.values[5] == 5).all()
    df = DataFrame(float_frame.values, copy=True)
    float_frame.values[6] = 6
    assert (not (df.values[6] == 6).all())