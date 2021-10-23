def check_bind_with_uniform(uf, gf, dim, sf=None, lshape=None, rshape=None):
    'check function consistency with uniform random numbers'
    shape = tuple(np.random.randint(1, int((1000 ** (1.0 / dim))), size=dim))
    lhs = mx.symbol.Variable('lhs')
    rhs = mx.symbol.Variable('rhs')
    if (sf is not None):
        ret = sf(lhs, rhs)
    else:
        ret = uf(lhs, rhs)
    assert (ret.list_arguments() == ['lhs', 'rhs'])
    lshape = (shape if (lshape is None) else lshape)
    rshape = (shape if (rshape is None) else rshape)
    lhs_arr = mx.nd.array(np.random.uniform((- 1), 1, lshape))
    rhs_arr = mx.nd.array(np.random.uniform((- 1), 1, rshape))
    lhs_grad = mx.nd.empty(lshape)
    rhs_grad = mx.nd.empty(rshape)
    executor = ret.bind(mx.Context('cpu'), args=[lhs_arr, rhs_arr], args_grad=[lhs_grad, rhs_grad])
    exec3 = ret.bind(mx.Context('cpu'), args=[lhs_arr, rhs_arr])
    exec4 = ret.bind(mx.Context('cpu'), args={
        'rhs': rhs_arr,
        'lhs': lhs_arr,
    }, args_grad={
        'lhs': lhs_grad,
        'rhs': rhs_grad,
    })
    executor.forward()
    exec3.forward()
    exec4.forward()
    out2 = executor.outputs[0].asnumpy()
    out1 = uf(lhs_arr.asnumpy(), rhs_arr.asnumpy())
    out3 = exec3.outputs[0].asnumpy()
    out4 = exec4.outputs[0].asnumpy()
    assert_almost_equal(out1, out2, rtol=1e-05, atol=1e-05)
    assert_almost_equal(out1, out3, rtol=1e-05, atol=1e-05)
    assert_almost_equal(out1, out4, rtol=1e-05, atol=1e-05)
    out_grad = mx.nd.array(np.ones(out2.shape))
    (lhs_grad2, rhs_grad2) = gf(out_grad.asnumpy(), lhs_arr.asnumpy(), rhs_arr.asnumpy())
    executor.backward([out_grad])
    assert_almost_equal(lhs_grad.asnumpy(), lhs_grad2, rtol=1e-05, atol=1e-05)
    assert_almost_equal(rhs_grad.asnumpy(), rhs_grad2, rtol=1e-05, atol=1e-05)