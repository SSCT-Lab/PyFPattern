def test_non_unique(self):
    idx = IntervalIndex.from_tuples([(1, 3), (3, 7)])
    s = pd.Series(range(len(idx)), index=idx)
    result = s.loc[Interval(1, 3)]
    assert (result == 0)
    result = s.loc[[Interval(1, 3)]]
    expected = s.iloc[0:1]
    tm.assert_series_equal(expected, result)