def test_agg_apply_evaluate_lambdas_the_same(self, string_series):
    result = string_series.apply((lambda x: str(x)))
    expected = string_series.agg((lambda x: str(x)))
    tm.assert_series_equal(result, expected)
    result = string_series.apply(str)
    expected = string_series.agg(str)
    tm.assert_series_equal(result, expected)