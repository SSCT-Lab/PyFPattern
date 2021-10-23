@with_seed()
@use_np
def test_np_mixed_precision_binary_funcs():

    def check_mixed_precision_binary_func(func, low, high, lshape, rshape, ltype, rtype):

        class TestMixedBinary(HybridBlock):

            def __init__(self, func):
                super(TestMixedBinary, self).__init__()
                self._func = func

            def hybrid_forward(self, F, a, b, *args, **kwargs):
                return getattr(F.np, self._func)(a, b)
        np_func = getattr(_np, func)
        mx_func = TestMixedBinary(func)
        np_test_x1 = _np.random.uniform(low, high, lshape).astype(ltype)
        np_test_x2 = _np.random.uniform(low, high, rshape).astype(rtype)
        mx_test_x1 = mx.numpy.array(np_test_x1, dtype=ltype)
        mx_test_x2 = mx.numpy.array(np_test_x2, dtype=rtype)
        rtol = (0.01 if ((ltype is np.float16) or (rtype is np.float16)) else 0.001)
        atol = (0.001 if ((ltype is np.float16) or (rtype is np.float16)) else 1e-05)
        for hybridize in [True, False]:
            if hybridize:
                mx_func.hybridize()
            np_out = np_func(np_test_x1, np_test_x2)
            with mx.autograd.record():
                y = mx_func(mx_test_x1, mx_test_x2)
            assert (y.shape == np_out.shape)
            assert_almost_equal(y.asnumpy(), np_out.astype(y.dtype), rtol=rtol, atol=atol, use_broadcast=False, equal_nan=True)
        np_out = getattr(_np, func)(np_test_x1, np_test_x2)
        mx_out = getattr(mx.np, func)(mx_test_x1, mx_test_x2)
        assert (mx_out.shape == np_out.shape)
        assert_almost_equal(mx_out.asnumpy(), np_out.astype(mx_out.dtype), rtol=rtol, atol=atol, use_broadcast=False, equal_nan=True)
    funcs = {
        'add': ((- 1.0), 1.0),
        'subtract': ((- 1.0), 1.0),
        'multiply': ((- 1.0), 1.0),
    }
    shape_pairs = [((3, 2), (3, 2)), ((3, 2), (3, 1)), ((3, 1), (3, 0)), ((0, 2), (1, 2)), ((2, 3, 4), (3, 1)), ((2, 3), ()), ((), (2, 3))]
    itypes = [np.bool, np.int8, np.int32, np.int64]
    ftypes = [np.float16, np.float32, np.float64]
    for (func, func_data) in funcs.items():
        (low, high) = func_data
        for (lshape, rshape) in shape_pairs:
            for (type1, type2) in itertools.product(itypes, ftypes):
                check_mixed_precision_binary_func(func, low, high, lshape, rshape, type1, type2)
                check_mixed_precision_binary_func(func, low, high, lshape, rshape, type2, type1)
            for (type1, type2) in itertools.product(ftypes, ftypes):
                if (type1 == type2):
                    continue
                check_mixed_precision_binary_func(func, low, high, lshape, rshape, type1, type2)