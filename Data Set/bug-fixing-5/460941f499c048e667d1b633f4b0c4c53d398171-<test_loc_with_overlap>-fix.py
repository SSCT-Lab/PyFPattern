def test_loc_with_overlap(self):
    idx = IntervalIndex.from_tuples([(1, 5), (3, 7)])
    s = Series(range(len(idx)), index=idx)
    expected = s
    result = s.loc[4]
    tm.assert_series_equal(expected, result)
    result = s[4]
    tm.assert_series_equal(expected, result)
    result = s.loc[[4]]
    tm.assert_series_equal(expected, result)
    result = s[[4]]
    tm.assert_series_equal(expected, result)
    expected = 0
    result = s.loc[Interval(1, 5)]
    tm.assert_series_equal(expected, result)
    result = s[Interval(1, 5)]
    tm.assert_series_equal(expected, result)
    expected = s
    result = s.loc[[Interval(1, 5), Interval(3, 7)]]
    tm.assert_series_equal(expected, result)
    result = s[[Interval(1, 5), Interval(3, 7)]]
    tm.assert_series_equal(expected, result)
    with pytest.raises(KeyError):
        s.loc[Interval(3, 5)]
    with pytest.raises(KeyError):
        s.loc[[Interval(3, 5)]]
    with pytest.raises(KeyError):
        s[Interval(3, 5)]
    with pytest.raises(KeyError):
        s[[Interval(3, 5)]]
    expected = s
    result = s.loc[Interval(1, 5):Interval(3, 7)]
    tm.assert_series_equal(expected, result)
    result = s[Interval(1, 5):Interval(3, 7)]
    tm.assert_series_equal(expected, result)
    with pytest.raises(KeyError):
        s.loc[Interval(1, 6):Interval(3, 8)]
    with pytest.raises(KeyError):
        s[Interval(1, 6):Interval(3, 8)]
    with pytest.raises(KeyError):
        s.loc[1:4]