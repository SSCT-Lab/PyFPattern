def test_reduce(self):
    result = self.series.agg(['sum', 'mean'])
    expected = Series([self.series.sum(), self.series.mean()], ['sum', 'mean'], name=self.series.name)
    assert_series_equal(result, expected)