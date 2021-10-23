

@pytest.mark.parametrize('dtype', [np.int64, np.int32, np.int16, np.int8])
def test_dti_constructor_small_int(self, dtype):
    exp = DatetimeIndex(['1970-01-01 00:00:00.00000000', '1970-01-01 00:00:00.00000001', '1970-01-01 00:00:00.00000002'])
    arr = np.array([0, 10, 20], dtype=dtype)
    tm.assert_index_equal(DatetimeIndex(arr), exp)
