

@pytest.mark.parametrize('cache', [True, False])
def test_string_na_nat_conversion(self, cache):
    strings = np.array(['1/1/2000', '1/2/2000', np.nan, '1/4/2000, 12:34:56'], dtype=object)
    expected = np.empty(4, dtype='M8[ns]')
    for (i, val) in enumerate(strings):
        if isna(val):
            expected[i] = iNaT
        else:
            expected[i] = parse(val)
    result = tslib.array_to_datetime(strings)[0]
    tm.assert_almost_equal(result, expected)
    result2 = to_datetime(strings, cache=cache)
    assert isinstance(result2, DatetimeIndex)
    tm.assert_numpy_array_equal(result, result2.values)
    malformed = np.array(['1/100/2000', np.nan], dtype=object)
    msg = "\\(u?'Unknown string format:', '1/100/2000'\\)|day is out of range for month"
    with pytest.raises(ValueError, match=msg):
        to_datetime(malformed, errors='raise', cache=cache)
    result = to_datetime(malformed, errors='ignore', cache=cache)
    expected = Index(malformed)
    tm.assert_index_equal(result, expected)
    with pytest.raises(ValueError, match=msg):
        to_datetime(malformed, errors='raise', cache=cache)
    idx = ['a', 'b', 'c', 'd', 'e']
    series = Series(['1/1/2000', np.nan, '1/3/2000', np.nan, '1/5/2000'], index=idx, name='foo')
    dseries = Series([to_datetime('1/1/2000', cache=cache), np.nan, to_datetime('1/3/2000', cache=cache), np.nan, to_datetime('1/5/2000', cache=cache)], index=idx, name='foo')
    result = to_datetime(series, cache=cache)
    dresult = to_datetime(dseries, cache=cache)
    expected = Series(np.empty(5, dtype='M8[ns]'), index=idx)
    for i in range(5):
        x = series[i]
        if isna(x):
            expected[i] = iNaT
        else:
            expected[i] = to_datetime(x, cache=cache)
    assert_series_equal(result, expected, check_names=False)
    assert (result.name == 'foo')
    assert_series_equal(dresult, expected, check_names=False)
    assert (dresult.name == 'foo')
