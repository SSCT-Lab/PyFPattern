def test_hfft(self):
    x = (random(14) + (1j * random(14)))
    x_herm = np.concatenate((random(1), x, random(1)))
    x = np.concatenate((x_herm, x[::(- 1)].conj()))
    assert_allclose(np.fft.fft(x), np.fft.hfft(x_herm), atol=1e-06)
    assert_allclose((np.fft.hfft(x_herm) / np.sqrt(30)), np.fft.hfft(x_herm, norm='ortho'), atol=1e-06)