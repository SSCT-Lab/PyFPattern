def test_values_numeric_cols(self):
    self.frame['foo'] = 'bar'
    values = self.frame[['A', 'B', 'C', 'D']].values
    assert (values.dtype == np.float64)