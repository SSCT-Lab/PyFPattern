def test_max(self, string_series):
    self._check_stat_op('max', np.max, string_series, check_objects=True)