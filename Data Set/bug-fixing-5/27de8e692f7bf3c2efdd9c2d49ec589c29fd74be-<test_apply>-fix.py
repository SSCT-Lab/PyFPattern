def test_apply(self, datetime_series):
    with np.errstate(all='ignore'):
        tm.assert_series_equal(datetime_series.apply(np.sqrt), np.sqrt(datetime_series))
        import math
        tm.assert_series_equal(datetime_series.apply(math.exp), np.exp(datetime_series))
    s = Series(dtype=object, name='foo', index=pd.Index([], name='bar'))
    rs = s.apply((lambda x: x))
    tm.assert_series_equal(s, rs)
    assert (s is not rs)
    assert (s.index is rs.index)
    assert (s.dtype == rs.dtype)
    assert (s.name == rs.name)
    s = Series(index=[1, 2, 3])
    rs = s.apply((lambda x: x))
    tm.assert_series_equal(s, rs)