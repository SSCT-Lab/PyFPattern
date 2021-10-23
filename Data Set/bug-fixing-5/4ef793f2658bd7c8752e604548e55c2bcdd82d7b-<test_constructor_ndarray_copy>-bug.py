def test_constructor_ndarray_copy(self):
    df = DataFrame(self.frame.values)
    self.frame.values[5] = 5
    assert (df.values[5] == 5).all()
    df = DataFrame(self.frame.values, copy=True)
    self.frame.values[6] = 6
    assert (not (df.values[6] == 6).all())