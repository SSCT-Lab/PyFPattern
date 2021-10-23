def test_replicate_describe(self):
    expected = self.series.describe()
    result = self.series.apply(OrderedDict([('count', 'count'), ('mean', 'mean'), ('std', 'std'), ('min', 'min'), ('25%', (lambda x: x.quantile(0.25))), ('50%', 'median'), ('75%', (lambda x: x.quantile(0.75))), ('max', 'max')]))
    assert_series_equal(result, expected)