def test_reindex_columns(self, float_frame):
    new_frame = float_frame.reindex(columns=['A', 'B', 'E'])
    tm.assert_series_equal(new_frame['B'], float_frame['B'])
    assert np.isnan(new_frame['E']).all()
    assert ('C' not in new_frame)
    new_frame = float_frame.reindex(columns=[])
    assert new_frame.empty