def test_besselk_int(self):
    assert_mpmath_equal(sc.kn, mpmath.besselk, [IntArg((- 200), 200), Arg(0, np.inf)], nan_ok=False, rtol=1e-12)