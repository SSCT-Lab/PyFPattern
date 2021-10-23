def test_besselk(self):
    assert_mpmath_equal(sc.kv, mpmath.besselk, [Arg((- 200), 200), Arg(0, np.inf)], nan_ok=False, rtol=1e-12)