def test_irfft2(self):
    x = random((30, 20))
    assert_allclose(x, np.fft.irfft2(np.fft.rfft2(x)), atol=1e-06)
    assert_allclose(x, np.fft.irfft2(np.fft.rfft2(x, norm='ortho'), norm='ortho'), atol=1e-06)