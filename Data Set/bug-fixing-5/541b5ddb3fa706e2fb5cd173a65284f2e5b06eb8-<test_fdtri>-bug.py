def test_fdtri(self):
    assert_allclose(cephes.fdtri(1, 1, [0.499, 0.5, 0.501]), array([0.9937365, 1.0, 1.00630298]), rtol=1e-06)
    p = 0.8756751669632106
    assert_allclose(cephes.fdtri(0.1, 1, p), 3, rtol=1e-12)