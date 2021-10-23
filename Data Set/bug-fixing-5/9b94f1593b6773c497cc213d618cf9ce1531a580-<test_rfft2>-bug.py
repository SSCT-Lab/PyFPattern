def test_rfft2(self):
    x = random((30, 20))
    assert_array_almost_equal(np.fft.fft2(x)[:, :11], np.fft.rfft2(x))
    assert_array_almost_equal((np.fft.rfft2(x) / np.sqrt((30 * 20))), np.fft.rfft2(x, norm='ortho'))