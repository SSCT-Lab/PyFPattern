def check_preloaded_multi_sgd(dtype, shapes, momentum, use_master_weights):

    def _flatten_list(nested_list):
        return [item for sublist in nested_list for item in sublist]
    weights_arr = [(np.random.rand(*shape).astype(dtype) * 100.0) for shape in shapes]
    grads_arr = [(np.random.rand(*shape).astype(dtype) * 100.0) for shape in shapes]
    rescale_grad = (np.random.random() + 1.0)
    mx_w = _make_ndarrays(weights_arr)
    mx_g = _make_ndarrays(grads_arr)
    mx_p_w = _make_ndarrays(weights_arr)
    mx_p_g = _make_ndarrays(grads_arr)
    lrs = list(((np.random.random(size=len(shapes)).astype('float32') + 0.1) / 100.0))
    mx_lrs = mx.nd.array(lrs, dtype='float32', ctx=mx.gpu(0))
    wds = list(((np.random.random(size=len(shapes)).astype('float32') + 0.1) / 1000.0))
    mx_wds = mx.nd.array(wds, dtype='float32', ctx=mx.gpu(0))
    if use_master_weights:
        weights32_arr = [arr.astype('float32') for arr in weights_arr]
        mx_w32 = _make_ndarrays(weights32_arr)
        mx_p_w32 = _make_ndarrays(weights32_arr)
    if (momentum is None):
        if use_master_weights:
            mx.nd.multi_mp_sgd_update(*_flatten_list(zip(mx_w, mx_g, mx_w32)), num_weights=len(shapes), lrs=lrs, wds=wds, rescale_grad=rescale_grad, out=mx_w)
            mx.nd.preloaded_multi_mp_sgd_update(*(_flatten_list(zip(mx_p_w, mx_p_g, mx_p_w32)) + [mx_lrs, mx_wds]), num_weights=len(shapes), rescale_grad=rescale_grad, out=mx_p_w)
        else:
            out = mx.nd.multi_sgd_update(*_flatten_list(zip(mx_w, mx_g)), num_weights=len(shapes), lrs=lrs, wds=wds, rescale_grad=rescale_grad, out=mx_w)
            preloaded_out = mx.nd.preloaded_multi_sgd_update(*(_flatten_list(zip(mx_p_w, mx_p_g)) + [mx_lrs, mx_wds]), num_weights=len(shapes), rescale_grad=rescale_grad, out=mx_p_w)
    elif use_master_weights:
        momentums_arr = [np.random.rand(*shape).astype('float32') for shape in shapes]
        mx_m = _make_ndarrays(momentums_arr)
        mx_p_m = _make_ndarrays(momentums_arr)
        out = mx.nd.multi_mp_sgd_mom_update(*_flatten_list(zip(mx_w, mx_g, mx_m, mx_w32)), num_weights=len(shapes), lrs=lrs, wds=wds, rescale_grad=0.95, momentum=momentum, out=mx_w)
        preloaded_out = mx.nd.preloaded_multi_mp_sgd_mom_update(*(_flatten_list(zip(mx_p_w, mx_p_g, mx_p_m, mx_p_w32)) + [mx_lrs, mx_wds]), num_weights=len(shapes), rescale_grad=0.95, momentum=momentum, out=mx_p_w)
    else:
        momentums_arr = [np.random.rand(*shape).astype(dtype) for shape in shapes]
        mx_m = _make_ndarrays(momentums_arr)
        mx_p_m = _make_ndarrays(momentums_arr)
        mx.nd.multi_sgd_mom_update(*_flatten_list(zip(mx_w, mx_g, mx_m)), num_weights=len(shapes), lrs=lrs, wds=wds, rescale_grad=0.95, momentum=momentum, out=mx_w)
        mx.nd.preloaded_multi_sgd_mom_update(*(_flatten_list(zip(mx_p_w, mx_p_g, mx_p_m)) + [mx_lrs, mx_wds]), num_weights=len(shapes), rescale_grad=0.95, momentum=momentum, out=mx_p_w)

    def _assert_all_almost_equal(lhs_list, rhs_list, rtol, atol):
        for (i, (lhs, rhs)) in enumerate(zip(lhs_list, rhs_list)):
            assert_almost_equal(lhs.asnumpy(), rhs.asnumpy(), rtol=rtol, atol=atol)
    if (dtype == 'float16'):
        rtol = 0.001
        atol = 0.001
    else:
        rtol = 1e-05
        atol = 1e-06
    _assert_all_almost_equal(mx_p_w, mx_w, rtol, atol)
    if (momentum is not None):
        _assert_all_almost_equal(mx_p_m, mx_m, rtol, atol)
    if use_master_weights:
        _assert_all_almost_equal(mx_p_w32, mx_w32, 1e-05, 1e-06)