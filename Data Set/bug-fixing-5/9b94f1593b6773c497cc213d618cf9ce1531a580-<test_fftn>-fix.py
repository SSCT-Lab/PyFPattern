def test_fftn(self):
    x = (random((30, 20, 10)) + (1j * random((30, 20, 10))))
    assert_allclose(np.fft.fft(np.fft.fft(np.fft.fft(x, axis=2), axis=1), axis=0), np.fft.fftn(x), atol=1e-06)
    assert_allclose((np.fft.fftn(x) / np.sqrt(((30 * 20) * 10))), np.fft.fftn(x, norm='ortho'), atol=1e-06)