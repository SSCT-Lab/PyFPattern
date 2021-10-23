@pytest.mark.parametrize('size, h_len, mode, dtype', product([8], [4, 5, 26], _upfirdn_modes, [np.float32, np.float64, np.complex64, np.complex128]))
def test_modes(self, size, h_len, mode, dtype):
    random_state = np.random.RandomState(5)
    x = random_state.randn(size).astype(dtype)
    if (dtype in (np.complex64, np.complex128)):
        x += (1j * random_state.randn(size))
    h = np.arange(1, (1 + h_len), dtype=x.real.dtype)
    y = upfirdn(h, x, up=1, down=1, mode=mode)
    npad = (h_len - 1)
    if (mode in ['antisymmetric', 'antireflect', 'smooth', 'line']):
        xpad = _pad_test(x, npre=npad, npost=npad, mode=mode)
    else:
        xpad = np.pad(x, npad, mode=mode)
    ypad = upfirdn(h, xpad, up=1, down=1, mode='constant')
    y_expected = ypad[npad:(- npad)]
    atol = rtol = (np.finfo(dtype).eps * 100.0)
    assert_allclose(y, y_expected, atol=atol, rtol=rtol)