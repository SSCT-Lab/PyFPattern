def _check_sampler_sampler(self, torch_dist, ref_dist, message, num_samples=10000, failure_rate=0.001):
    torch_samples = torch_dist.sample_n(num_samples).squeeze().cpu().numpy()
    ref_samples = ref_dist.rvs(num_samples)
    samples = ([(x, (+ 1)) for x in torch_samples] + [(x, (- 1)) for x in ref_samples])
    samples.sort()
    samples = np.array(samples)[:, 1]
    num_bins = 10
    samples_per_bin = (len(samples) // num_bins)
    bins = samples.reshape((num_bins, samples_per_bin)).mean(axis=1)
    stddev = (samples_per_bin ** (- 0.5))
    threshold = (stddev * scipy.special.erfinv((1 - ((2 * failure_rate) / num_bins))))
    message = '{}.sample() is biased:\n{}'.format(message, bins)
    for bias in bins:
        self.assertLess((- threshold), bias, message)
        self.assertLess(bias, threshold, message)