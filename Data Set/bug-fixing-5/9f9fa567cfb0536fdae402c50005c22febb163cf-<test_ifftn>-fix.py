def test_ifftn(self):
    x = (random((30, 20, 10)) + (1j * random((30, 20, 10))))
    assert_allclose(np.fft.ifft(np.fft.ifft(np.fft.ifft(x, axis=2), axis=1), axis=0), np.fft.ifftn(x), atol=1e-06)
    assert_allclose((np.fft.ifftn(x) * np.sqrt(((30 * 20) * 10))), np.fft.ifftn(x, norm='ortho'), atol=1e-06)