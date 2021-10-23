def test_mvn_pdf(self):
    cov3 = self.cov3
    mvn3 = self.mvn3
    r_val = [(- 7.667977543898155), (- 6.917977543898155), (- 5.167977543898155)]
    assert_array_almost_equal(mvn3.logpdf(cov3), r_val, decimal=14)
    r_val = [0.000467562492721686, 0.000989829804859273, 0.005696077243833402]
    assert_array_almost_equal(mvn3.pdf(cov3), r_val, decimal=17)
    mvn3b = MVNormal(np.array([0, 0, 0]), cov3)
    r_val = [0.02914269740502042, 0.02269635555984291, 0.01767593948287269]
    assert_array_almost_equal(mvn3b.pdf(cov3), r_val, decimal=16)