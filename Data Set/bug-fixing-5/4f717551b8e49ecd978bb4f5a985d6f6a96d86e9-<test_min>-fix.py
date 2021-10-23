def test_min(self, string_series):
    self._check_stat_op('min', np.min, string_series, check_objects=True)