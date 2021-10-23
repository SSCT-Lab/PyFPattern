def test_dti_constructor_small_int(self, any_int_dtype):
    exp = DatetimeIndex(['1970-01-01 00:00:00.00000000', '1970-01-01 00:00:00.00000001', '1970-01-01 00:00:00.00000002'])
    arr = np.array([0, 10, 20], dtype=any_int_dtype)
    tm.assert_index_equal(DatetimeIndex(arr), exp)