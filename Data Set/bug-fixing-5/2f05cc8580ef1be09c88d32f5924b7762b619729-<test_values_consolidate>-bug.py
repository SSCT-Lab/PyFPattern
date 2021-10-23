def test_values_consolidate(self):
    self.frame['E'] = 7.0
    assert (not self.frame._data.is_consolidated())
    _ = self.frame.values
    assert self.frame._data.is_consolidated()