@testing.parametrize('seed', [1, 2, 3, 5, 8, 13])
def test_ssim_grad(seed):
    N = 30
    rnd = np.random.RandomState(seed)
    X = (rnd.rand(N, N) * 255)
    Y = (rnd.rand(N, N) * 255)
    f = ssim(X, Y, data_range=255)
    g = ssim(X, Y, data_range=255, gradient=True)
    assert (f < 0.05)
    assert (g[0] < 0.05)
    assert np.all((g[1] < 0.05))
    (mssim, grad, s) = ssim(X, Y, data_range=255, gradient=True, full=True)
    assert np.all((grad < 0.05))