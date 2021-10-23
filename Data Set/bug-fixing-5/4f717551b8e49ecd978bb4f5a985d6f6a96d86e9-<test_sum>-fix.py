def test_sum(self, string_series):
    self._check_stat_op('sum', np.sum, string_series, check_allna=False)