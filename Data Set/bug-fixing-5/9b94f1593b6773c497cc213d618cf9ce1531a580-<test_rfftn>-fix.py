def test_rfftn(self):
    x = random((30, 20, 10))
    assert_allclose(np.fft.fftn(x)[:, :, :6], np.fft.rfftn(x), atol=1e-06)
    assert_allclose((np.fft.rfftn(x) / np.sqrt(((30 * 20) * 10))), np.fft.rfftn(x, norm='ortho'), atol=1e-06)