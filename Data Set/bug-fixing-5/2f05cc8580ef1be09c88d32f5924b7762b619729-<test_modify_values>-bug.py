def test_modify_values(self):
    self.frame.values[5] = 5
    assert (self.frame.values[5] == 5).all()
    self.frame['E'] = 7.0
    self.frame.values[6] = 6
    assert (self.frame.values[6] == 6).all()