def test_irfft2(self):
    x = random((30, 20))
    assert_array_almost_equal(x, np.fft.irfft2(np.fft.rfft2(x)))
    assert_array_almost_equal(x, np.fft.irfft2(np.fft.rfft2(x, norm='ortho'), norm='ortho'))