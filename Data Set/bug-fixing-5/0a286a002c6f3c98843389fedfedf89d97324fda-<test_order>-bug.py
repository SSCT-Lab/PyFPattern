@with_seed()
def test_order():
    ctx = default_context()
    dat_size = 5

    def gt_topk(dat, axis, ret_typ, k, is_ascend):
        if (ret_typ == 'indices'):
            if is_ascend:
                indices = np.arange(k)
            else:
                indices = np.arange((- 1), ((- k) - 1), (- 1))
            ret = np.take(dat.argsort(axis=axis), axis=axis, indices=indices, mode='wrap')
        elif (ret_typ == 'value'):
            if is_ascend:
                indices = np.arange(k)
            else:
                indices = np.arange((- 1), ((- k) - 1), (- 1))
            ret = np.take(np.sort(dat, axis=axis), axis=axis, indices=indices, mode='wrap')
        else:
            assert (dat.shape == (dat_size, dat_size, dat_size, dat_size))
            assert ((axis is None) or (axis == 1))
            ret = np.zeros(dat.shape)
            if is_ascend:
                indices = np.arange(k)
            else:
                indices = np.arange((- 1), ((- k) - 1), (- 1))
            gt_argsort = np.take(dat.argsort(axis=axis), axis=axis, indices=indices, mode='wrap')
            if (axis is None):
                ret.ravel()[gt_argsort] = 1
            else:
                for i in range(dat_size):
                    for j in range(dat_size):
                        for k in range(dat_size):
                            ret[(i, gt_argsort[i, :, j, k], j, k)] = 1
        return ret

    def get_values(ensure_unique, dtype):
        if ((dtype == np.int16) or (dtype == np.int32) or (dtype == np.int64)):
            return np.arange((dat_size ** 4), dtype=dtype).reshape((dat_size, dat_size, dat_size, dat_size))
        elif ((dtype == np.float32) or (dtype == np.float64)):
            while True:
                data = np.random.normal(size=(dat_size, dat_size, dat_size, dat_size)).astype(dtype)
                if (not ensure_unique):
                    return data
                num_unique_values = len(set(data.flatten()))
                if (data.size == num_unique_values):
                    return data
        else:
            raise NotImplementedError

    def get_large_matrix():
        data = np.array([np.arange(300096).astype(np.float32)])
        data = np.repeat(data, 100, axis=0)
        np.apply_along_axis(np.random.shuffle, 1, data)
        return data
    large_matrix_npy = get_large_matrix()
    large_matrix_nd = mx.nd.array(large_matrix_npy, ctx=ctx)
    nd_ret_topk = mx.nd.topk(large_matrix_nd, axis=1, ret_typ='indices', k=5, is_ascend=False).asnumpy()
    gt = gt_topk(large_matrix_npy, axis=1, ret_typ='indices', k=5, is_ascend=False)
    assert_almost_equal(nd_ret_topk, gt)
    for dtype in [np.int16, np.int32, np.int64, np.float32, np.float64]:
        a_npy = get_values(ensure_unique=True, dtype=dtype)
        a_nd = mx.nd.array(a_npy, ctx=ctx)
        nd_ret_topk = mx.nd.topk(a_nd, axis=1, ret_typ='indices', k=3, is_ascend=True).asnumpy()
        gt = gt_topk(a_npy, axis=1, ret_typ='indices', k=3, is_ascend=True)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=3, ret_typ='indices', k=2, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=3, ret_typ='indices', k=2, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=None, ret_typ='indices', k=21, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=None, ret_typ='indices', k=21, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=1, ret_typ='value', k=3, is_ascend=True).asnumpy()
        gt = gt_topk(a_npy, axis=1, ret_typ='value', k=3, is_ascend=True)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=3, ret_typ='value', k=2, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=3, ret_typ='value', k=2, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=None, ret_typ='value', k=21, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=None, ret_typ='value', k=21, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=1, ret_typ='mask', k=3, is_ascend=True).asnumpy()
        gt = gt_topk(a_npy, axis=1, ret_typ='mask', k=3, is_ascend=True)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=1, ret_typ='mask', k=2, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=1, ret_typ='mask', k=2, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=None, ret_typ='mask', k=21, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=None, ret_typ='mask', k=21, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        (nd_ret_topk_val, nd_ret_topk_ind) = mx.nd.topk(a_nd, axis=1, ret_typ='both', k=3, is_ascend=True)
        nd_ret_topk_val = nd_ret_topk_val.asnumpy()
        nd_ret_topk_ind = nd_ret_topk_ind.asnumpy()
        gt_val = gt_topk(a_npy, axis=1, ret_typ='value', k=3, is_ascend=True)
        gt_ind = gt_topk(a_npy, axis=1, ret_typ='indices', k=3, is_ascend=True)
        assert_almost_equal(nd_ret_topk_val, gt_val)
        assert_almost_equal(nd_ret_topk_ind, gt_ind)
        (_, nd_ret_topk_ind) = mx.nd.topk(a_nd, axis=1, ret_typ='both', k=3, is_ascend=True)
        nd_ret_topk_ind = nd_ret_topk_ind.asnumpy()
        assert_almost_equal(nd_ret_topk_ind, gt_ind)
        (nd_ret_topk_val, _) = mx.nd.topk(a_nd, axis=1, ret_typ='both', k=3, is_ascend=True)
        nd_ret_topk_val = nd_ret_topk_val.asnumpy()
        assert_almost_equal(nd_ret_topk_val, gt_val)
        nd_ret_sort = mx.nd.sort(a_nd, axis=1, is_ascend=True).asnumpy()
        gt = gt_topk(a_npy, axis=1, ret_typ='value', k=dat_size, is_ascend=True)
        assert_almost_equal(nd_ret_sort, gt)
        nd_ret_sort = mx.nd.sort(a_nd, axis=None, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=None, ret_typ='value', k=(((dat_size * dat_size) * dat_size) * dat_size), is_ascend=False)
        assert_almost_equal(nd_ret_sort, gt)
        for idtype in [np.int32, np.float16, np.float32, np.float64]:
            nd_ret_argsort = mx.nd.argsort(a_nd, axis=3, is_ascend=True, dtype=idtype).asnumpy()
            gt = gt_topk(a_npy, axis=3, ret_typ='indices', k=dat_size, is_ascend=True)
            assert_almost_equal(nd_ret_argsort, gt)
            nd_ret_argsort = mx.nd.argsort(a_nd, axis=None, is_ascend=False, dtype=idtype).asnumpy()
            gt = gt_topk(a_npy, axis=None, ret_typ='indices', k=(((dat_size * dat_size) * dat_size) * dat_size), is_ascend=False)
            assert_almost_equal(nd_ret_argsort, gt)
        a_npy = get_values(ensure_unique=False, dtype=dtype)
        a_nd = mx.nd.array(a_npy, ctx=ctx)
        nd_ret_topk = mx.nd.topk(a_nd, axis=1, ret_typ='value', k=3, is_ascend=True).asnumpy()
        gt = gt_topk(a_npy, axis=1, ret_typ='value', k=3, is_ascend=True)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=3, ret_typ='value', k=2, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=3, ret_typ='value', k=2, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=None, ret_typ='value', k=21, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=None, ret_typ='value', k=21, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_sort = mx.nd.sort(a_nd, axis=1, is_ascend=True).asnumpy()
        gt = gt_topk(a_npy, axis=1, ret_typ='value', k=dat_size, is_ascend=True)
        assert_almost_equal(nd_ret_sort, gt)
        nd_ret_sort = mx.nd.sort(a_nd, axis=None, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=None, ret_typ='value', k=(((dat_size * dat_size) * dat_size) * dat_size), is_ascend=False)
        assert_almost_equal(nd_ret_sort, gt)
    a = mx.nd.arange(0, 1024, step=1, repeat=1, dtype=np.int32)
    assert_almost_equal(a.topk(k=1024, dtype=np.int32).asnumpy(), a.asnumpy()[::(- 1)])
    a.attach_grad()
    k = 10
    with mx.autograd.record():
        b = mx.nd.topk(a, k=k, ret_typ='value')
        b.backward(mx.nd.ones((k,), dtype=np.int32))
    a_grad = a.grad.asnumpy()
    for i in range((- 1), ((- k) - 1), (- 1)):
        assert (a_grad[i] == 1)
    for dtype in [np.int32, np.int64, np.float32, np.float64]:
        a = mx.nd.arange(0, 1000, step=1, repeat=1, dtype=dtype)
        a.attach_grad()
        k = 10
        ograd = mx.nd.arange(0, k, dtype=dtype)
        with mx.autograd.record():
            b = mx.nd.topk(a, k=k, ret_typ='value')
            b.backward(ograd)
        a_grad = a.grad.asnumpy()
        ograd_npy = ograd.asnumpy()
        for i in range((- 1), ((- k) - 1), (- 1)):
            assert (a_grad[i] == ograd_npy[((- i) - 1)])
    for dtype in [np.int16, np.int32, np.int64, np.float32, np.float64]:
        a_npy = get_values(ensure_unique=False, dtype=dtype)
        a_nd = mx.nd.array(a_npy, ctx=ctx)
        nd_ret_topk = mx.nd.topk(a_nd, axis=1, ret_typ='value', k=3, is_ascend=True).asnumpy()
        gt = gt_topk(a_npy, axis=1, ret_typ='value', k=3, is_ascend=True)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=3, ret_typ='value', k=2, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=3, ret_typ='value', k=2, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_topk = mx.nd.topk(a_nd, axis=None, ret_typ='value', k=21, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=None, ret_typ='value', k=21, is_ascend=False)
        assert_almost_equal(nd_ret_topk, gt)
        nd_ret_sort = mx.nd.sort(a_nd, axis=1, is_ascend=True).asnumpy()
        gt = gt_topk(a_npy, axis=1, ret_typ='value', k=dat_size, is_ascend=True)
        assert_almost_equal(nd_ret_sort, gt)
        nd_ret_sort = mx.nd.sort(a_nd, axis=None, is_ascend=False).asnumpy()
        gt = gt_topk(a_npy, axis=None, ret_typ='value', k=(((dat_size * dat_size) * dat_size) * dat_size), is_ascend=False)
        assert_almost_equal(nd_ret_sort, gt)