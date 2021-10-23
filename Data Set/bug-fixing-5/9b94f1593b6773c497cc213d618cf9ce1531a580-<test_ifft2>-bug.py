def test_ifft2(self):
    x = (random((30, 20)) + (1j * random((30, 20))))
    assert_array_almost_equal(np.fft.ifft(np.fft.ifft(x, axis=1), axis=0), np.fft.ifft2(x))
    assert_array_almost_equal((np.fft.ifft2(x) * np.sqrt((30 * 20))), np.fft.ifft2(x, norm='ortho'))