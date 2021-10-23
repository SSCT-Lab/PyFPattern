def test_expm1_complex(self):
    assert_mpmath_equal(sc.expm1, mpmath.expm1, [ComplexArg()])