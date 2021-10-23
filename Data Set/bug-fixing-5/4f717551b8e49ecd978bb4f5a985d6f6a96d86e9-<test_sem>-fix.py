def test_sem(self, datetime_series, string_series):
    alt = (lambda x: (np.std(x, ddof=1) / np.sqrt(len(x))))
    self._check_stat_op('sem', alt, string_series)
    result = datetime_series.sem(ddof=4)
    expected = (np.std(datetime_series.values, ddof=4) / np.sqrt(len(datetime_series.values)))
    assert_almost_equal(result, expected)
    s = datetime_series.iloc[[0]]
    result = s.sem(ddof=1)
    assert isna(result)