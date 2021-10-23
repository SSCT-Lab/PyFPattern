def test_error_too_many_dims(self):
    m = memoryview(self.c_u8_33d())
    assert_equal(m.ndim, 33)
    assert_raises_regex(RuntimeError, 'ndim', np.array, m)