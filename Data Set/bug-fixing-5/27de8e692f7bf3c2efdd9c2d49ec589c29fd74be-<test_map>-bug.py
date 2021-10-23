def test_map(self):
    (index, data) = tm.getMixedTypeDict()
    source = Series(data['B'], index=data['C'])
    target = Series(data['C'][:4], index=data['D'][:4])
    merged = target.map(source)
    for (k, v) in compat.iteritems(merged):
        assert (v == source[target[k]])
    merged = target.map(source.to_dict())
    for (k, v) in compat.iteritems(merged):
        assert (v == source[target[k]])
    result = self.ts.map((lambda x: (x * 2)))
    tm.assert_series_equal(result, (self.ts * 2))
    a = Series([1, 2, 3, 4])
    b = Series(['even', 'odd', 'even', 'odd'], dtype='category')
    c = Series(['even', 'odd', 'even', 'odd'])
    exp = Series(['odd', 'even', 'odd', np.nan], dtype='category')
    tm.assert_series_equal(a.map(b), exp)
    exp = Series(['odd', 'even', 'odd', np.nan])
    tm.assert_series_equal(a.map(c), exp)
    a = Series(['a', 'b', 'c', 'd'])
    b = Series([1, 2, 3, 4], index=pd.CategoricalIndex(['b', 'c', 'd', 'e']))
    c = Series([1, 2, 3, 4], index=Index(['b', 'c', 'd', 'e']))
    exp = Series([np.nan, 1, 2, 3])
    tm.assert_series_equal(a.map(b), exp)
    exp = Series([np.nan, 1, 2, 3])
    tm.assert_series_equal(a.map(c), exp)
    a = Series(['a', 'b', 'c', 'd'])
    b = Series(['B', 'C', 'D', 'E'], dtype='category', index=pd.CategoricalIndex(['b', 'c', 'd', 'e']))
    c = Series(['B', 'C', 'D', 'E'], index=Index(['b', 'c', 'd', 'e']))
    exp = Series(pd.Categorical([np.nan, 'B', 'C', 'D'], categories=['B', 'C', 'D', 'E']))
    tm.assert_series_equal(a.map(b), exp)
    exp = Series([np.nan, 'B', 'C', 'D'])
    tm.assert_series_equal(a.map(c), exp)