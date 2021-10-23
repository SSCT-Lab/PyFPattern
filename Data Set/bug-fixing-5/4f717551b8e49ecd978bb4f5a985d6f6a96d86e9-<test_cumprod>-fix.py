def test_cumprod(self, datetime_series):
    self._check_accum_op('cumprod', datetime_series)