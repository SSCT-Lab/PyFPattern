def test_identity(self):
    maxlen = 512
    x = (random(maxlen) + (1j * random(maxlen)))
    xr = random(maxlen)
    for i in range(1, maxlen):
        assert_allclose(np.fft.ifft(np.fft.fft(x[0:i])), x[0:i], atol=1e-12)
        assert_allclose(np.fft.irfft(np.fft.rfft(xr[0:i]), i), xr[0:i], atol=1e-12)