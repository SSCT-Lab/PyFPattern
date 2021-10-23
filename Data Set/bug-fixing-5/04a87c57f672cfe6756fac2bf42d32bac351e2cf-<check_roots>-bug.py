def check_roots(Poly):
    d = (Poly.domain + (random((2,)) * 0.25))
    w = (Poly.window + (random((2,)) * 0.25))
    tgt = np.sort(random((5,)))
    res = np.sort(Poly.fromroots(tgt, domain=d, window=w).roots())
    assert_almost_equal(res, tgt)
    res = np.sort(Poly.fromroots(tgt).roots())
    assert_almost_equal(res, tgt)