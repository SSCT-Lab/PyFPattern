def test_ffill(self, datetime_frame):
    datetime_frame['A'][:5] = np.nan
    datetime_frame['A'][(- 5):] = np.nan
    assert_frame_equal(datetime_frame.ffill(), datetime_frame.fillna(method='ffill'))