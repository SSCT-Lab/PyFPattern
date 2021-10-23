@pytest.mark.parametrize('dtype', [np.half, np.single, np.double, np.longdouble])
def test_dtypes(self, dtype):
    x = random(30).astype(dtype)
    assert_array_almost_equal(np.fft.ifft(np.fft.fft(x)), x)
    assert_array_almost_equal(np.fft.irfft(np.fft.rfft(x)), x)