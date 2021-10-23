def test_values_consolidate(self, float_frame):
    float_frame['E'] = 7.0
    assert (not float_frame._data.is_consolidated())
    _ = float_frame.values
    assert float_frame._data.is_consolidated()