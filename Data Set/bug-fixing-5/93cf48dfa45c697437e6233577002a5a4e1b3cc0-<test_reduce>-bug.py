@with_seed()
def test_reduce():
    sample_num = 300

    def test_reduce_inner(numpy_reduce_func, nd_reduce_func, multi_axes, allow_almost_equal=False, check_dtype=True):
        dtypes = [(np.float16, 1), (np.float32, 5), (np.double, 6)]
        for i in range(sample_num):
            (dtype, decimal) = random.choice(dtypes)
            ndim = np.random.randint(1, 6)
            shape = np.random.randint(1, 11, size=ndim)
            dat = (np.random.rand(*shape) - 0.5).astype(dtype)
            keepdims = np.random.randint(0, 2)
            allow_nan = np.random.randint(0, 2)
            if allow_nan:
                total_nans = np.random.randint(0, ((dat.size // 10) + 1))
                dat.ravel()[np.random.choice(dat.size, total_nans, replace=False)] = np.nan
            allow_inf = np.random.randint(0, 2)
            if allow_inf:
                r = np.random.randint(0, 3)
                total_infs = np.random.randint(0, ((dat.size // 20) + 1))
                if (r == 0):
                    (total_pos_infs, total_neg_infs) = (total_infs, 0)
                elif (r == 1):
                    (total_pos_infs, total_neg_infs) = (0, total_infs)
                else:
                    total_pos_infs = total_neg_infs = (total_infs // 2)
                dat.ravel()[np.random.choice(dat.size, total_pos_infs, replace=False)] = np.inf
                dat.ravel()[np.random.choice(dat.size, total_neg_infs, replace=False)] = (- np.inf)
            if multi_axes:
                axis_flags = np.random.randint(0, 2, size=ndim)
                axes = []
                for (axis, flag) in enumerate(axis_flags):
                    if flag:
                        axes.append(axis)
                if (0 == len(axes)):
                    axes = tuple(range(ndim))
                else:
                    axes = tuple(axes)
            else:
                axes = np.random.randint(0, ndim)
            numpy_ret = numpy_reduce_func(dat, axis=axes, keepdims=keepdims)
            mx_arr = mx.nd.array(dat, dtype=dtype)
            ndarray_ret = nd_reduce_func(mx_arr, axis=axes, keepdims=keepdims)
            if (type(ndarray_ret) is mx.ndarray.NDArray):
                ndarray_ret = ndarray_ret.asnumpy()
            assert ((ndarray_ret.shape == numpy_ret.shape) or ((ndarray_ret.shape == (1,)) and (numpy_ret.shape == ()))), ('nd:%s, numpy:%s' % (ndarray_ret.shape, numpy_ret.shape))
            if check_dtype:
                assert (ndarray_ret.dtype == numpy_ret.dtype), (ndarray_ret.dtype, numpy_ret.dtype)
            if allow_almost_equal:
                assert_array_almost_equal(ndarray_ret, numpy_ret, decimal=decimal)
            else:
                assert_array_equal(ndarray_ret, numpy_ret)
    test_reduce_inner((lambda data, axis, keepdims: np_reduce(data, axis, keepdims, np.sum)), mx.nd.sum, True, allow_almost_equal=True)
    test_reduce_inner((lambda data, axis, keepdims: np_reduce(data, axis, keepdims, np.max)), mx.nd.max, True)
    test_reduce_inner((lambda data, axis, keepdims: np_reduce(data, axis, keepdims, np.min)), mx.nd.min, True)
    test_reduce_inner((lambda data, axis, keepdims: np_reduce(np.float32(data), axis, keepdims, np.argmax)), mx.nd.argmax, False, check_dtype=False)
    test_reduce_inner((lambda data, axis, keepdims: np_reduce(np.float32(data), axis, keepdims, np.argmin)), mx.nd.argmin, False, check_dtype=False)