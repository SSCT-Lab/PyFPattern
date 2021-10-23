def test_consolidate_deprecation(self, float_frame):
    float_frame['E'] = 7
    with tm.assert_produces_warning(FutureWarning):
        float_frame.consolidate()