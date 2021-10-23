def test_reindex_columns(self):
    new_frame = self.frame.reindex(columns=['A', 'B', 'E'])
    tm.assert_series_equal(new_frame['B'], self.frame['B'])
    assert np.isnan(new_frame['E']).all()
    assert ('C' not in new_frame)
    new_frame = self.frame.reindex(columns=[])
    assert new_frame.empty