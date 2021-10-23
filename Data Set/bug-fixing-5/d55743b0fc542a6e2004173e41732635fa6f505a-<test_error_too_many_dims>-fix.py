def test_error_too_many_dims(self):

    def make_ctype(shape, scalar_type):
        t = scalar_type
        for dim in shape[::(- 1)]:
            t = (dim * t)
        return t
    c_u8_33d = make_ctype(((1,) * 33), ctypes.c_uint8)
    m = memoryview(c_u8_33d())
    assert_equal(m.ndim, 33)
    assert_raises_regex(RuntimeError, 'ndim', np.array, m)