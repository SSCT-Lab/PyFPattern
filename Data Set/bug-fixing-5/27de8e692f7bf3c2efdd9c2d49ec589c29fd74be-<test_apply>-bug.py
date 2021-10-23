def test_apply(self):
    with np.errstate(all='ignore'):
        tm.assert_series_equal(self.ts.apply(np.sqrt), np.sqrt(self.ts))
        import math
        tm.assert_series_equal(self.ts.apply(math.exp), np.exp(self.ts))
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