def test_values_lcd(self, mixed_float_frame, mixed_int_frame):
    values = mixed_float_frame[['A', 'B', 'C', 'D']].values
    assert (values.dtype == np.float64)
    values = mixed_float_frame[['A', 'B', 'C']].values
    assert (values.dtype == np.float32)
    values = mixed_float_frame[['C']].values
    assert (values.dtype == np.float16)
    values = mixed_int_frame[['A', 'B', 'C', 'D']].values
    assert (values.dtype == np.float64)
    values = mixed_int_frame[['A', 'D']].values
    assert (values.dtype == np.int64)
    values = mixed_int_frame[['A', 'B', 'C']].values
    assert (values.dtype == np.float64)
    values = mixed_int_frame[['B', 'C']].values
    assert (values.dtype == np.uint64)
    values = mixed_int_frame[['A', 'C']].values
    assert (values.dtype == np.int32)
    values = mixed_int_frame[['C', 'D']].values
    assert (values.dtype == np.int64)
    values = mixed_int_frame[['A']].values
    assert (values.dtype == np.int32)
    values = mixed_int_frame[['C']].values
    assert (values.dtype == np.uint8)