def test_besselk_int(self):
    assert_mpmath_equal(sc.kn, exception_to_nan((lambda v, z: mpmath.besselk(v, z, **HYPERKW))), [IntArg((- 1000), 1000), Arg()])