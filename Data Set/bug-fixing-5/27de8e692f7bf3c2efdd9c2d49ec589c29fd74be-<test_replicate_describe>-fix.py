def test_replicate_describe(self, string_series):
    expected = string_series.describe()
    result = string_series.apply(OrderedDict([('count', 'count'), ('mean', 'mean'), ('std', 'std'), ('min', 'min'), ('25%', (lambda x: x.quantile(0.25))), ('50%', 'median'), ('75%', (lambda x: x.quantile(0.75))), ('max', 'max')]))
    assert_series_equal(result, expected)