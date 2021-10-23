

def test_compare_nonnested(self):
    res = self.res
    res2 = self.res2
    jtest = [('M1 + fitted(M2)', 1.591505670785873, 0.7384552861695823, 2.15518217635237, 0.03235457252531445, '*'), ('M2 + fitted(M1)', 1.305687653016899, 0.4808385176653064, 2.715438978051544, 0.007203854534057954, '**')]
    jt1 = smsdia.compare_j(res2, res)
    assert_almost_equal(jt1, jtest[0][3:5], decimal=13)
    jt2 = smsdia.compare_j(res, res2)
    assert_almost_equal(jt2, jtest[1][3:5], decimal=13)
    coxtest = [('fitted(M1) ~ M2', (- 0.782030488930356), 0.599696502782265, (- 1.304043770977755), 0.1922186587840554, ' '), ('fitted(M2) ~ M1', (- 2.248817107408537), 0.392656854330139, (- 5.727181590258883), 1.021128495098556e-08, '***')]
    ct1 = smsdia.compare_cox(res, res2)
    assert_almost_equal(ct1, coxtest[0][3:5], decimal=12)
    ct2 = smsdia.compare_cox(res2, res)
    assert_almost_equal(ct2, coxtest[1][3:5], decimal=12)
    encomptest = [('M1 vs. ME', 198, (- 1), 4.644810213266983, 0.032354572525313666, '*'), ('M2 vs. ME', 198, (- 1), 7.373608843521585, 0.007203854534058054, '**')]
    petest = [('M1 + log(fit(M1))-fit(M2)', (- 229.2818783545946), 44.50878220870586, (- 5.15139), 6.201281252449979e-07), ('M2 + fit(M1)-exp(fit(M2))', 0.000634664704814, 4.62387010349e-05, 13.72583, 1.319536115230356e-30)]
