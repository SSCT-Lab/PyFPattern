def test_consolidate(self):
    self.frame['E'] = 7.0
    consolidated = self.frame._consolidate()
    assert (len(consolidated._data.blocks) == 1)
    recons = consolidated._consolidate()
    assert (recons is not consolidated)
    tm.assert_frame_equal(recons, consolidated)
    self.frame['F'] = 8.0
    assert (len(self.frame._data.blocks) == 3)
    self.frame._consolidate(inplace=True)
    assert (len(self.frame._data.blocks) == 1)