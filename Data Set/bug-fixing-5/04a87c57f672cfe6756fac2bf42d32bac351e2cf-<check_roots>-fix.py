def check_roots(Poly):
    d = ((Poly.domain * 1.25) + 0.25)
    w = Poly.window
    tgt = np.linspace(d[0], d[1], 5)
    res = np.sort(Poly.fromroots(tgt, domain=d, window=w).roots())
    assert_almost_equal(res, tgt)
    res = np.sort(Poly.fromroots(tgt).roots())
    assert_almost_equal(res, tgt)