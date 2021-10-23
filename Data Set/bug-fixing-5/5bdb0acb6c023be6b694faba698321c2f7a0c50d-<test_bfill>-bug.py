def test_bfill(self):
    self.tsframe['A'][:5] = np.nan
    self.tsframe['A'][(- 5):] = np.nan
    assert_frame_equal(self.tsframe.bfill(), self.tsframe.fillna(method='bfill'))