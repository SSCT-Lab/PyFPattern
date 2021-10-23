def test_enumerate_support_type(self):
    for (Dist, params) in EXAMPLES:
        for (i, param) in enumerate(params):
            dist = Dist(**param)
            try:
                self.assertTrue((type(unwrap(dist.sample())) is type(unwrap(dist.enumerate_support()))), msg=('{} example {}/{}, return type mismatch between ' + 'sample and enumerate_support.').format(Dist.__name__, i, len(params)))
            except NotImplementedError:
                pass