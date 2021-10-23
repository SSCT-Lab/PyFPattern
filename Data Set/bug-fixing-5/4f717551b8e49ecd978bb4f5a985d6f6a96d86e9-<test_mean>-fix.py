def test_mean(self, string_series):
    self._check_stat_op('mean', np.mean, string_series)