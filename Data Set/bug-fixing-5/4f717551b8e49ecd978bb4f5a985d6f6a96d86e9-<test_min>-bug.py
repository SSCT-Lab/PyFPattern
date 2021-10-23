def test_min(self):
    self._check_stat_op('min', np.min, check_objects=True)