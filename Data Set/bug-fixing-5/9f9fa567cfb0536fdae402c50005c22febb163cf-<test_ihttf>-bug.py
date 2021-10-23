def test_ihttf(self):
    x = (random(14) + (1j * random(14)))
    x_herm = np.concatenate((random(1), x, random(1)))
    x = np.concatenate((x_herm, x[::(- 1)].conj()))
    assert_array_almost_equal(x_herm, np.fft.ihfft(np.fft.hfft(x_herm)))
    assert_array_almost_equal(x_herm, np.fft.ihfft(np.fft.hfft(x_herm, norm='ortho'), norm='ortho'))