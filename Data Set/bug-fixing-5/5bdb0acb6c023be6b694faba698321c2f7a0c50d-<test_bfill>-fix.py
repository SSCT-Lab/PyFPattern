def test_bfill(self, datetime_frame):
    datetime_frame['A'][:5] = np.nan
    datetime_frame['A'][(- 5):] = np.nan
    assert_frame_equal(datetime_frame.bfill(), datetime_frame.fillna(method='bfill'))