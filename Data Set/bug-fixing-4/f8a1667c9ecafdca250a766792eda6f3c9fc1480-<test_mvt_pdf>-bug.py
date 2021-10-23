def test_mvt_pdf(self):
    cov3 = self.cov3
    mu3 = self.mu3
    mvt = MVT((0, 0), 1, 5)
    assert_almost_equal(mvt.logpdf(np.array([0.0, 0.0])), (- 1.837877066409345), decimal=15)
    assert_almost_equal(mvt.pdf(np.array([0.0, 0.0])), 0.1591549430918953, decimal=15)
    (mvt.logpdf(np.array([1.0, 1.0])) - (- 3.01552989458359))
    mvt1 = MVT((0, 0), 1, 1)
    (mvt1.logpdf(np.array([1.0, 1.0])) - (- 3.48579549941151))
    rvs = mvt.rvs(100000)
    assert_almost_equal(np.cov(rvs, rowvar=0), mvt.cov, decimal=1)
    mvt31 = MVT(mu3, cov3, 1)
    assert_almost_equal(mvt31.pdf(cov3), [0.0007276818698165781, 0.0009980625182293658, 0.0027661422056214652], decimal=17)
    mvt = MVT(mu3, cov3, 3)
    assert_almost_equal(mvt.pdf(cov3), [0.00086377742424741, 0.001277510788307594, 0.004156314279452241], decimal=17)