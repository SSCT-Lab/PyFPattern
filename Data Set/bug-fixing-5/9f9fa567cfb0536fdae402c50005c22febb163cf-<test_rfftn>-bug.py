def test_rfftn(self):
    x = random((30, 20, 10))
    assert_array_almost_equal(np.fft.fftn(x)[:, :, :6], np.fft.rfftn(x))
    assert_array_almost_equal((np.fft.rfftn(x) / np.sqrt(((30 * 20) * 10))), np.fft.rfftn(x, norm='ortho'))