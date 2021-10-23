def test_copy(self):
    cop = self.frame.copy()
    cop['E'] = cop['A']
    assert ('E' not in self.frame)
    copy = self.mixed_frame.copy()
    assert (copy._data is not self.mixed_frame._data)