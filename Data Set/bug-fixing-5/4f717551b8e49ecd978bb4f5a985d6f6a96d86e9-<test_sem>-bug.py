def test_sem(self):
    alt = (lambda x: (np.std(x, ddof=1) / np.sqrt(len(x))))
    self._check_stat_op('sem', alt)
    result = self.ts.sem(ddof=4)
    expected = (np.std(self.ts.values, ddof=4) / np.sqrt(len(self.ts.values)))
    assert_almost_equal(result, expected)
    s = self.ts.iloc[[0]]
    result = s.sem(ddof=1)
    assert isna(result)