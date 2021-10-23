def test_missing(self):
    N = 10
    rng = date_range('1/1/1990', periods=N, freq='53s')
    df = DataFrame({
        'A': np.arange(N),
        'B': np.arange(N),
    }, index=rng)
    result = df.asof('1989-12-31')
    expected = Series(index=['A', 'B'], name=Timestamp('1989-12-31'))
    tm.assert_series_equal(result, expected)
    result = df.asof(to_datetime(['1989-12-31']))
    expected = DataFrame(index=to_datetime(['1989-12-31']), columns=['A', 'B'], dtype='float64')
    tm.assert_frame_equal(result, expected)