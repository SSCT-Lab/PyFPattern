def test_cumsum(self, datetime_series):
    self._check_accum_op('cumsum', datetime_series)