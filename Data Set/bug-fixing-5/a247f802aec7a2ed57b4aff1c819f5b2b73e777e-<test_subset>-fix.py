def test_subset(self, date_range_frame):
    N = 10
    df = date_range_frame.iloc[:N].copy()
    df.loc[4:8, 'A'] = np.nan
    dates = date_range('1/1/1990', periods=(N * 3), freq='25s')
    result = df.asof(dates, subset='A')
    expected = df.asof(dates)
    tm.assert_frame_equal(result, expected)
    result = df.asof(dates, subset=['A', 'B'])
    expected = df.asof(dates)
    tm.assert_frame_equal(result, expected)
    result = df.asof(dates, subset='B')
    expected = df.resample('25s', closed='right').ffill().reindex(dates)
    expected.iloc[20:] = 9
    tm.assert_frame_equal(result, expected)