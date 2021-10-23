def test_sum(self):
    self._check_stat_op('sum', np.sum, check_allna=False)