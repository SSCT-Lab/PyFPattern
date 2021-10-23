def test_fftn(self):
    x = (random((30, 20, 10)) + (1j * random((30, 20, 10))))
    assert_array_almost_equal(np.fft.fft(np.fft.fft(np.fft.fft(x, axis=2), axis=1), axis=0), np.fft.fftn(x))
    assert_array_almost_equal((np.fft.fftn(x) / np.sqrt(((30 * 20) * 10))), np.fft.fftn(x, norm='ortho'))