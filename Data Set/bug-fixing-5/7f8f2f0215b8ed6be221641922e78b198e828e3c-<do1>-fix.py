@staticmethod
def do1(fname, ties, entry_f, strata_f):
    (time, status, entry, exog) = TestPHReg.load_file(fname)
    n = len(time)
    vs = fname.split('_')
    n = int(vs[2])
    p = int(vs[3].split('.')[0])
    ties1 = ties[0:3]
    strata = np.kron(range(5), np.ones((n // 5)))
    mod = PHReg(time, exog, status, ties=ties)
    phrb = mod.fit(**args)
    (coef_r, se_r, time_r, hazard_r) = get_results(n, p, None, ties1)
    assert_allclose(phrb.params, coef_r, rtol=0.001)
    assert_allclose(phrb.bse, se_r, rtol=0.0001)
    (time_h, cumhaz, surv) = phrb.baseline_cumulative_hazard[0]
    phrb = PHReg(time, exog, status, entry=entry, ties=ties).fit(**args)
    (coef, se, time_r, hazard_r) = get_results(n, p, 'et', ties1)
    assert_allclose(phrb.params, coef, rtol=0.001)
    assert_allclose(phrb.bse, se, rtol=0.001)
    phrb = PHReg(time, exog, status, strata=strata, ties=ties).fit(**args)
    (coef, se, time_r, hazard_r) = get_results(n, p, 'st', ties1)
    assert_allclose(phrb.params, coef, rtol=0.0001)
    assert_allclose(phrb.bse, se, rtol=0.0001)
    phrb = PHReg(time, exog, status, entry=entry, strata=strata, ties=ties).fit(**args)
    (coef, se, time_r, hazard_r) = get_results(n, p, 'et_st', ties1)
    assert_allclose(phrb.params, coef, rtol=0.001)
    assert_allclose(phrb.bse, se, rtol=0.0001)
    (time_h, cumhaz, surv) = phrb.baseline_cumulative_hazard[0]