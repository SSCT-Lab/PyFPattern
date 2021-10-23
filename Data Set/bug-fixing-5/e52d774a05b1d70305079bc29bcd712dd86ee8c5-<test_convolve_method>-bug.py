def test_convolve_method(self, n=100):
    types = sum([t for (_, t) in np.sctypes.items()], [])
    types = {np.dtype(t).name for t in types}
    for dtype in ['complex256', 'float128', 'str', 'void', 'bytes', 'object', 'unicode', 'string']:
        if (dtype in types):
            types.remove(dtype)
    args = [(t1, t2, mode) for t1 in types for t2 in types for mode in ['valid', 'full', 'same']]
    np.random.seed(42)
    array_types = {
        'i': np.random.choice([0, 1], size=n),
        'f': np.random.randn(n),
    }
    array_types['b'] = array_types['u'] = array_types['i']
    array_types['c'] = (array_types['f'] + (0.5j * array_types['f']))
    for (t1, t2, mode) in args:
        x1 = array_types[np.dtype(t1).kind].astype(t1)
        x2 = array_types[np.dtype(t2).kind].astype(t2)
        results = {key: convolve(x1, x2, method=key, mode=mode) for key in ['fft', 'direct']}
        assert_equal(results['fft'].dtype, results['direct'].dtype)
        if (('bool' in t1) and ('bool' in t2)):
            assert_equal(choose_conv_method(x1, x2), 'direct')
            continue
        if any([(t in {'complex64', 'float32'}) for t in [t1, t2]]):
            kwargs = {
                'rtol': 0.0001,
                'atol': 1e-06,
            }
        elif ('float16' in [t1, t2]):
            kwargs = {
                'rtol': 0.001,
                'atol': 1e-08,
            }
        else:
            kwargs = {
                'rtol': 1e-05,
                'atol': 1e-08,
            }
        assert_allclose(results['fft'], results['direct'], **kwargs)