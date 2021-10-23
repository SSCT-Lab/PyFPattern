def test_max(self):
    self._check_stat_op('max', np.max, check_objects=True)