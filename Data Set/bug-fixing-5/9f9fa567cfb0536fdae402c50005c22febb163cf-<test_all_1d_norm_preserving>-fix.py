def test_all_1d_norm_preserving(self):
    x = random(30)
    x_norm = np.linalg.norm(x)
    n = (x.size * 2)
    func_pairs = [(np.fft.fft, np.fft.ifft), (np.fft.rfft, np.fft.irfft), (np.fft.ihfft, np.fft.hfft)]
    for (forw, back) in func_pairs:
        for n in [x.size, (2 * x.size)]:
            for norm in [None, 'ortho']:
                tmp = forw(x, n=n, norm=norm)
                tmp = back(tmp, n=n, norm=norm)
                assert_allclose(x_norm, np.linalg.norm(tmp), atol=1e-06)