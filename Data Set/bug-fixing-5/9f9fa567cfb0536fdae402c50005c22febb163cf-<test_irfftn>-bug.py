def test_irfftn(self):
    x = random((30, 20, 10))
    assert_array_almost_equal(x, np.fft.irfftn(np.fft.rfftn(x)))
    assert_array_almost_equal(x, np.fft.irfftn(np.fft.rfftn(x, norm='ortho'), norm='ortho'))