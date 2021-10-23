def test_entropy_monte_carlo(self):
    set_rng_seed(0)
    for (Dist, params) in EXAMPLES:
        for (i, param) in enumerate(params):
            dist = Dist(**param)
            try:
                actual = dist.entropy()
            except NotImplementedError:
                continue
            x = dist.sample(sample_shape=(20000,))
            expected = (- dist.log_prob(x).mean(0))
            if isinstance(actual, Variable):
                actual = actual.data
                expected = expected.data
            ignore = (expected == float('inf'))
            expected[ignore] = actual[ignore]
            self.assertEqual(actual, expected, prec=0.2, message='\n'.join(['{} example {}/{}, incorrect .entropy().'.format(Dist.__name__, (i + 1), len(params)), 'Expected (monte carlo) {}'.format(expected), 'Actual (analytic) {}'.format(actual), 'max error = {}'.format(torch.abs((actual - expected)).max())]))