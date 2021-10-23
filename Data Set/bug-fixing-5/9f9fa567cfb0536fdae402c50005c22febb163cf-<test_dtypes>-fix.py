@pytest.mark.parametrize('dtype', [np.half, np.single, np.double, np.longdouble])
def test_dtypes(self, dtype):
    x = random(30).astype(dtype)
    assert_allclose(np.fft.ifft(np.fft.fft(x)), x, atol=1e-06)
    assert_allclose(np.fft.irfft(np.fft.rfft(x)), x, atol=1e-06)