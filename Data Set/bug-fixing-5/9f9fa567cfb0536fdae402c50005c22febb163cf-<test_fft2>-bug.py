def test_fft2(self):
    x = (random((30, 20)) + (1j * random((30, 20))))
    assert_array_almost_equal(np.fft.fft(np.fft.fft(x, axis=1), axis=0), np.fft.fft2(x))
    assert_array_almost_equal((np.fft.fft2(x) / np.sqrt((30 * 20))), np.fft.fft2(x, norm='ortho'))