def test_fillna(self):
    ts = Series([0.0, 1.0, 2.0, 3.0, 4.0], index=tm.makeDateIndex(5))
    tm.assert_series_equal(ts, ts.fillna(method='ffill'))
    ts[2] = np.NaN
    exp = Series([0.0, 1.0, 1.0, 3.0, 4.0], index=ts.index)
    tm.assert_series_equal(ts.fillna(method='ffill'), exp)
    exp = Series([0.0, 1.0, 3.0, 3.0, 4.0], index=ts.index)
    tm.assert_series_equal(ts.fillna(method='backfill'), exp)
    exp = Series([0.0, 1.0, 5.0, 3.0, 4.0], index=ts.index)
    tm.assert_series_equal(ts.fillna(value=5), exp)
    pytest.raises(ValueError, ts.fillna)
    pytest.raises(ValueError, self.ts.fillna, value=0, method='ffill')
    s1 = Series([np.nan])
    s2 = Series([1])
    result = s1.fillna(s2)
    expected = Series([1.0])
    assert_series_equal(result, expected)
    result = s1.fillna({
        
    })
    assert_series_equal(result, s1)
    result = s1.fillna(Series(()))
    assert_series_equal(result, s1)
    result = s2.fillna(s1)
    assert_series_equal(result, s2)
    result = s1.fillna({
        0: 1,
    })
    assert_series_equal(result, expected)
    result = s1.fillna({
        1: 1,
    })
    assert_series_equal(result, Series([np.nan]))
    result = s1.fillna({
        0: 1,
        1: 1,
    })
    assert_series_equal(result, expected)
    result = s1.fillna(Series({
        0: 1,
        1: 1,
    }))
    assert_series_equal(result, expected)
    result = s1.fillna(Series({
        0: 1,
        1: 1,
    }, index=[4, 5]))
    assert_series_equal(result, s1)
    s1 = Series([0, 1, 2], list('abc'))
    s2 = Series([0, np.nan, 2], list('bac'))
    result = s2.fillna(s1)
    expected = Series([0, 0, 2.0], list('bac'))
    assert_series_equal(result, expected)
    s = Series(np.nan, index=[0, 1, 2])
    result = s.fillna(999, limit=1)
    expected = Series([999, np.nan, np.nan], index=[0, 1, 2])
    assert_series_equal(result, expected)
    result = s.fillna(999, limit=2)
    expected = Series([999, 999, np.nan], index=[0, 1, 2])
    assert_series_equal(result, expected)
    vals = ['0', '1.5', '-0.3']
    for val in vals:
        s = Series([0, 1, np.nan, np.nan, 4], dtype='float64')
        result = s.fillna(val)
        expected = Series([0, 1, val, val, 4], dtype='object')
        assert_series_equal(result, expected)