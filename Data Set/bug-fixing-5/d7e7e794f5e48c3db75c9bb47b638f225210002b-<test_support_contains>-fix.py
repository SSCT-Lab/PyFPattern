def test_support_contains(self):
    for (Dist, params) in EXAMPLES:
        self.assertIsInstance(Dist.support, Constraint)
        for (i, param) in enumerate(params):
            dist = Dist(**param)
            value = dist.sample()
            constraint = dist.support
            message = '{} example {}/{} sample = {}'.format(Dist.__name__, (i + 1), len(params), value)
            self.assertTrue(constraint.check(value).all(), msg=message)