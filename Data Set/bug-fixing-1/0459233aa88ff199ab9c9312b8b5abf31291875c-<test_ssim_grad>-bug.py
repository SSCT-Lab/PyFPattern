

def test_ssim_grad():
    N = 30
    X = (np.random.rand(N, N) * 255)
    Y = (np.random.rand(N, N) * 255)
    f = ssim(X, Y, data_range=255)
    g = ssim(X, Y, data_range=255, gradient=True)
    assert (f < 0.05)
    assert (g[0] < 0.05)
    assert np.all((g[1] < 0.05))
    (mssim, grad, s) = ssim(X, Y, data_range=255, gradient=True, full=True)
    assert np.all((grad < 0.05))
