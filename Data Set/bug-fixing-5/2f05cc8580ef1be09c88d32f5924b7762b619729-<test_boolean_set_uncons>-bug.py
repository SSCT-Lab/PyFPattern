def test_boolean_set_uncons(self):
    self.frame['E'] = 7.0
    expected = self.frame.values.copy()
    expected[(expected > 1)] = 2
    self.frame[(self.frame > 1)] = 2
    assert_almost_equal(expected, self.frame.values)