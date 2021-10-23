def test_missing(self, date_range_frame):
    N = 10
    df = date_range_frame.iloc[:N].copy()
    result = df.asof('1989-12-31')
    expected = Series(index=['A', 'B'], name=Timestamp('1989-12-31'))
    tm.assert_series_equal(result, expected)
    result = df.asof(to_datetime(['1989-12-31']))
    expected = DataFrame(index=to_datetime(['1989-12-31']), columns=['A', 'B'], dtype='float64')
    tm.assert_frame_equal(result, expected)