def test_values_lcd(self):
    values = self.mixed_float[['A', 'B', 'C', 'D']].values
    assert (values.dtype == np.float64)
    values = self.mixed_float[['A', 'B', 'C']].values
    assert (values.dtype == np.float32)
    values = self.mixed_float[['C']].values
    assert (values.dtype == np.float16)
    values = self.mixed_int[['A', 'B', 'C', 'D']].values
    assert (values.dtype == np.float64)
    values = self.mixed_int[['A', 'D']].values
    assert (values.dtype == np.int64)
    values = self.mixed_int[['A', 'B', 'C']].values
    assert (values.dtype == np.float64)
    values = self.mixed_int[['B', 'C']].values
    assert (values.dtype == np.uint64)
    values = self.mixed_int[['A', 'C']].values
    assert (values.dtype == np.int32)
    values = self.mixed_int[['C', 'D']].values
    assert (values.dtype == np.int64)
    values = self.mixed_int[['A']].values
    assert (values.dtype == np.int32)
    values = self.mixed_int[['C']].values
    assert (values.dtype == np.uint8)