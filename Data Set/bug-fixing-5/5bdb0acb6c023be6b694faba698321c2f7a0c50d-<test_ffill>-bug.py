def test_ffill(self):
    self.tsframe['A'][:5] = np.nan
    self.tsframe['A'][(- 5):] = np.nan
    assert_frame_equal(self.tsframe.ffill(), self.tsframe.fillna(method='ffill'))