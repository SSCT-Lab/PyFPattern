def test_values_numeric_cols(self, float_frame):
    float_frame['foo'] = 'bar'
    values = float_frame[['A', 'B', 'C', 'D']].values
    assert (values.dtype == np.float64)