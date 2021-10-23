def test_consolidate_deprecation(self):
    self.frame['E'] = 7
    with tm.assert_produces_warning(FutureWarning):
        self.frame.consolidate()