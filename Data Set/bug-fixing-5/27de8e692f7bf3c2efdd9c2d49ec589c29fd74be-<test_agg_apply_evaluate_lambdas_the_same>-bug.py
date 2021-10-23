def test_agg_apply_evaluate_lambdas_the_same(self):
    result = self.series.apply((lambda x: str(x)))
    expected = self.series.agg((lambda x: str(x)))
    tm.assert_series_equal(result, expected)
    result = self.series.apply(str)
    expected = self.series.agg(str)
    tm.assert_series_equal(result, expected)