def test_irfftn(self):
    x = random((30, 20, 10))
    assert_allclose(x, np.fft.irfftn(np.fft.rfftn(x)), atol=1e-06)
    assert_allclose(x, np.fft.irfftn(np.fft.rfftn(x, norm='ortho'), norm='ortho'), atol=1e-06)