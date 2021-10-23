

def test_zero_dim(self):
    _test_reshape(old_shape=(4, 2, 1), new_shape=(0, 0, 0), expected_shape=(4, 2, 1))
    _test_reshape(old_shape=(4, 2, 1), new_shape=(0, 0, 0), expected_shape=(4, 2, 1), arg_shape=False)
    _test_reshape(old_shape=(4, 2, 1), new_shape=(0, 2, 1), expected_shape=(4, 2, 1))
    _test_reshape(old_shape=(4, 2, 1), new_shape=(0, 2, 1), expected_shape=(4, 2, 1), arg_shape=False)
