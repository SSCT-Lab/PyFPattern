def test_reduce(self, string_series):
    result = string_series.agg(['sum', 'mean'])
    expected = Series([string_series.sum(), string_series.mean()], ['sum', 'mean'], name=string_series.name)
    assert_series_equal(result, expected)