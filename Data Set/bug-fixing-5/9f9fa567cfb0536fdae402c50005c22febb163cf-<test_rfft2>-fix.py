def test_rfft2(self):
    x = random((30, 20))
    assert_allclose(np.fft.fft2(x)[:, :11], np.fft.rfft2(x), atol=1e-06)
    assert_allclose((np.fft.rfft2(x) / np.sqrt((30 * 20))), np.fft.rfft2(x, norm='ortho'), atol=1e-06)