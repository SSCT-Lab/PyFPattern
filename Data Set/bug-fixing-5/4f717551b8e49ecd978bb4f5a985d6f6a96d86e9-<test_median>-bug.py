def test_median(self):
    self._check_stat_op('median', np.median)
    int_ts = Series(np.ones(10, dtype=int), index=lrange(10))
    tm.assert_almost_equal(np.median(int_ts), int_ts.median())