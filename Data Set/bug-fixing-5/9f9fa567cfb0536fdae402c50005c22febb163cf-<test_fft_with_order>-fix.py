@pytest.mark.parametrize('dtype', [np.float32, np.float64, np.complex64, np.complex128])
@pytest.mark.parametrize('order', ['F', 'non-contiguous'])
@pytest.mark.parametrize('fft', [np.fft.fft, np.fft.fft2, np.fft.fftn, np.fft.ifft, np.fft.ifft2, np.fft.ifftn])
def test_fft_with_order(dtype, order, fft):
    rng = np.random.RandomState(42)
    X = rng.rand(8, 7, 13).astype(dtype, copy=False)
    _tol = ((8.0 * np.sqrt(np.log2(X.size))) * np.finfo(X.dtype).eps)
    if (order == 'F'):
        Y = np.asfortranarray(X)
    else:
        Y = X[::(- 1)]
        X = np.ascontiguousarray(X[::(- 1)])
    if fft.__name__.endswith('fft'):
        for axis in range(3):
            X_res = fft(X, axis=axis)
            Y_res = fft(Y, axis=axis)
            assert_allclose(X_res, Y_res, atol=_tol, rtol=_tol)
    elif fft.__name__.endswith(('fft2', 'fftn')):
        axes = [(0, 1), (1, 2), (0, 2)]
        if fft.__name__.endswith('fftn'):
            axes.extend([(0,), (1,), (2,), None])
        for ax in axes:
            X_res = fft(X, axes=ax)
            Y_res = fft(Y, axes=ax)
            assert_allclose(X_res, Y_res, atol=_tol, rtol=_tol)
    else:
        raise ValueError()