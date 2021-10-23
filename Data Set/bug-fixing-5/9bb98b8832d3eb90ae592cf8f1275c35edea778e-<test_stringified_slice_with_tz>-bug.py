def test_stringified_slice_with_tz(self):
    import datetime
    start = datetime.datetime.now()
    idx = date_range(start=start, freq='1d', periods=10, tz='US/Eastern')
    df = DataFrame(lrange(10), index=idx)
    df['2013-01-14 23:44:34.437768-05:00':]