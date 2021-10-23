def test_consolidate(self, float_frame):
    float_frame['E'] = 7.0
    consolidated = float_frame._consolidate()
    assert (len(consolidated._data.blocks) == 1)
    recons = consolidated._consolidate()
    assert (recons is not consolidated)
    tm.assert_frame_equal(recons, consolidated)
    float_frame['F'] = 8.0
    assert (len(float_frame._data.blocks) == 3)
    float_frame._consolidate(inplace=True)
    assert (len(float_frame._data.blocks) == 1)