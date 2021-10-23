def test_copy(self, float_frame, float_string_frame):
    cop = float_frame.copy()
    cop['E'] = cop['A']
    assert ('E' not in float_frame)
    copy = float_string_frame.copy()
    assert (copy._data is not float_string_frame._data)