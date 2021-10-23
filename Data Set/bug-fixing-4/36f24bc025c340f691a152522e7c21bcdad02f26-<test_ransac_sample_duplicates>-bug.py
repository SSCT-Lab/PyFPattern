def test_ransac_sample_duplicates():

    class DummyModel(object):
        'Dummy model to check for duplicates.'

        def estimate(self, data):
            assert_equal(np.unique(data).size, data.size)
            return True

        def residuals(self, data):
            return 1.0
    data = np.arange(4)
    ransac(data, DummyModel, min_samples=3, residual_threshold=0.0, max_trials=10)