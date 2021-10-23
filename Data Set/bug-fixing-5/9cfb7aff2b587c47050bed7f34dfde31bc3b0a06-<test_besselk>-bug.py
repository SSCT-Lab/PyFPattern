def test_besselk(self):

    def mpbesselk(v, x):
        r = float(mpmath.besselk(v, x, **HYPERKW))
        if (abs(r) > 1e+305):
            r = (np.inf * np.sign(r))
        if ((abs(v) == abs(x)) and (abs(r) == np.inf) and (abs(x) > 1)):
            old_dps = mpmath.mp.dps
            mpmath.mp.dps = 200
            try:
                r = float(mpmath.besselk(v, x, **HYPERKW))
            finally:
                mpmath.mp.dps = old_dps
        return r
    assert_mpmath_equal(sc.kv, exception_to_nan(mpbesselk), [Arg((- 1e+100), 1e+100), Arg()])