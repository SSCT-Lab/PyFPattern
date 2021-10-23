@unittest.skipIf((not TEST_NUMPY), 'Numpy not found')
def test_beta_log_prob(self):
    for _ in range(100):
        alpha = np.exp(np.random.normal())
        beta = np.exp(np.random.normal())
        dist = Beta(alpha, beta)
        x = dist.sample()
        actual_log_prob = dist.log_prob(x).sum()
        expected_log_prob = scipy.stats.beta.logpdf(x, alpha, beta)[0]
        self.assertAlmostEqual(actual_log_prob, expected_log_prob, places=3)