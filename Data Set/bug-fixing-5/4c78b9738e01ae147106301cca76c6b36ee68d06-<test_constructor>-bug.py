def test_constructor(self):
    assert self.ts.index.is_all_dates
    derived = Series(self.ts)
    assert derived.index.is_all_dates
    assert tm.equalContents(derived.index, self.ts.index)
    assert (id(self.ts.index) == id(derived.index))
    mixed = Series(['hello', np.NaN], index=[0, 1])
    assert (mixed.dtype == np.object_)
    assert (mixed[1] is np.NaN)
    assert (not self.empty.index.is_all_dates)
    assert (not Series({
        
    }).index.is_all_dates)
    pytest.raises(Exception, Series, np.random.randn(3, 3), index=np.arange(3))
    mixed.name = 'Series'
    rs = Series(mixed).name
    xp = 'Series'
    assert (rs == xp)
    m = MultiIndex.from_arrays([[1, 2], [3, 4]])
    pytest.raises(NotImplementedError, Series, m)