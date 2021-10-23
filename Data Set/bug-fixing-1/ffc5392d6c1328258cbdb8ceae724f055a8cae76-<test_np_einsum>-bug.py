

@with_seed()
@use_np
def test_np_einsum():

    class TestEinsum(HybridBlock):

        def __init__(self, subscripts, optimize):
            super(TestEinsum, self).__init__()
            self.subscripts = subscripts
            self.optimize = optimize

        def hybrid_forward(self, F, *operands):
            return F.np.einsum(self.subscripts, *operands, optimize=self.optimize)

    def dbg(name, data):
        print('type of {} = {}'.format(name, type(data)))
        print('shape of {} = {}'.format(name, data.shape))
        print('{} = {}'.format(name, data))
    configs = [('ii', [(5, 5)], (lambda *args: (_np.eye(5),))), ('ii->i', [(5, 5)], (lambda *args: (_np.eye(5),))), ('ij->i', [(5, 5)], (lambda *args: (_np.ones((5, 5)),))), ('...j->...', [(5, 5)], (lambda *args: (_np.ones((5, 5)),))), ('ji', [(2, 3)], (lambda *args: (_np.ones((2, 3)),))), ('ij->ji', [(2, 3)], (lambda *args: (_np.ones((2, 3)),))), ('i, i', [(5,), (5,)], (lambda *args: (args[1], args[0]))), ('ij, j', [(5, 5), (5,)], (lambda *args: (_np.tile(args[1][None, :], [5, 1]), args[0].sum(axis=0)))), ('...j, j', [(5, 5), (5,)], (lambda *args: (_np.tile(args[1][None, :], [5, 1]), _np.sum(args[0], axis=0)))), ('..., ...', [(), (2, 3)], (lambda *args: (_np.sum(args[1], axis=None), (args[0] * _np.ones((2, 3)))))), (', ij', [(), (2, 3)], (lambda *args: (_np.sum(args[1], axis=None), (args[0] * _np.ones((2, 3)))))), ('i, j', [(2,), (5,)], (lambda *args: ((_np.sum(args[1], axis=None) * _np.ones(2)), (_np.sum(args[0], axis=None) * _np.ones(5))))), ('ijk, jil->kl', [(3, 4, 5), (4, 3, 2)], (lambda *args: (_np.tile(_np.transpose(_np.sum(args[1], axis=(- 1)))[:, :, None], [1, 1, 5]), _np.tile(_np.transpose(_np.sum(args[0], axis=(- 1)))[:, :, None], [1, 1, 2])))), ('ii->i', [(3, 3)], (lambda *args: (_np.eye(3),))), ('ki, jk->ij', [(3, 2), (4, 3)], (lambda *args: (_np.tile(args[1].sum(axis=0)[:, None], [1, 2]), _np.tile(args[0].sum(axis=1)[None, :], [4, 1])))), ('ki, ...k->i...', [(3, 2), (4, 3)], (lambda *args: (_np.tile(args[1].sum(axis=0)[:, None], [1, 2]), _np.tile(args[0].sum(axis=1)[None, :], [4, 1])))), ('k..., jk', [(3, 2), (4, 3)], (lambda *args: (_np.tile(args[1].sum(axis=0)[:, None], [1, 2]), _np.tile(args[0].sum(axis=1)[None, :], [4, 1])))), ('ij, jk', [(5, 0), (0, 4)], (lambda *args: (_np.empty((5, 0)), _np.empty((0, 4))))), ('ij,jk,kl->il', [(2, 2), (2, 5), (5, 2)], (lambda *args: (_np.dot(_np.ones((2, 2)), _np.dot(args[1], args[2]).T), _np.dot(args[0].T, _np.dot(_np.ones((2, 2)), args[2].T)), _np.dot(_np.dot(args[0], args[1]).T, _np.ones((2, 2)))))), ('ij, ij -> i', [(1, 4), (2, 4)], (lambda *args: (_np.sum(args[1], axis=0)[None, :], _np.tile(args[0], [2, 1]))))]
    dtypes = ['float16', 'float32', 'float64', 'int32']
    acc_type = {
        'float16': 'float32',
        'float32': 'float64',
        'float64': 'float64',
        'int32': 'int64',
    }
    for hybridize in [False, True]:
        for dtype in dtypes:
            for config in configs:
                for optimize in [False, True]:
                    rtol = (0.01 if (dtype == 'float16') else 0.001)
                    atol = (0.0001 if (dtype == 'float16') else 1e-05)
                    (subscripts, operands, get_grad) = config
                    test_einsum = TestEinsum(subscripts, optimize)
                    if hybridize:
                        test_einsum.hybridize()
                    x = []
                    x_np = []
                    for shape in operands:
                        tmp = _np.array(_np.random.uniform((- 1.0), 1.0, shape), dtype=dtype)
                        x_np.append(tmp.astype(acc_type[dtype]))
                        x.append(np.array(tmp, dtype=dtype))
                        x[(- 1)].attach_grad()
                    expected_np = _np.einsum(subscripts, *x_np, optimize=optimize).astype(dtype)
                    with mx.autograd.record():
                        out_mx = test_einsum(*x)
                    assert (out_mx.shape == expected_np.shape)
                    assert_almost_equal(out_mx.asnumpy(), expected_np, rtol=rtol, atol=atol)
                    out_mx.backward()
                    for (iop, op) in enumerate(x):
                        assert_almost_equal(op.grad.asnumpy(), get_grad(*x_np)[iop], rtol=rtol, atol=atol)
                    for op in x:
                        op.attach_grad()
                    with mx.autograd.record():
                        out_mx = np.einsum(subscripts, *x, optimize=optimize)
                    out_mx.backward()
                    expected_np = _np.einsum(subscripts, *x_np, optimize=optimize)
                    assert_almost_equal(out_mx.asnumpy(), expected_np, rtol=rtol, atol=atol)
                    for (iop, op) in enumerate(x):
                        assert_almost_equal(op.grad.asnumpy(), get_grad(*x_np)[iop].astype(dtype), rtol=rtol, atol=atol)
    configs = [('ij,jk,kl->il', [(2, 2), (2, 5), (5, 2)]), ('ea,fb,abcd,gc,hd->efgh', [(5, 5), (5, 5), (5, 5, 5, 5), (5, 5), (5, 5)])]
    dtypes = ['int32', 'float32', 'float64']
    for hybridize in [False, True]:
        for dtype in dtypes:
            for config in configs:
                (subscripts, operands) = config
                rtol = (0.01 if (dtype == 'float16') else 0.001)
                atol = (0.0001 if (dtype == 'float16') else 1e-05)
                grad = []
                x_np = []
                for shape in operands:
                    x_np.append(_np.array(_np.random.uniform((- 2.0), 2.0, shape), dtype=dtype))
                for optimize in [False, True]:
                    x = []
                    for (iop, op) in enumerate(operands):
                        x.append(np.array(x_np[iop], dtype=dtype))
                        x[(- 1)].attach_grad()
                    test_einsum = TestEinsum(subscripts, optimize)
                    if hybridize:
                        test_einsum.hybridize()
                    expected_np = _np.einsum(subscripts, *[op.astype(acc_type[dtype]) for op in x_np], optimize=optimize).astype(dtype)
                    with mx.autograd.record():
                        out_mx = test_einsum(*x)
                    assert (out_mx.shape == expected_np.shape)
                    assert_almost_equal(out_mx.asnumpy(), expected_np, rtol=rtol, atol=atol)
                    out_mx.backward()
                    cur_grad = []
                    for (iop, op) in enumerate(x):
                        cur_grad.append(op.grad.asnumpy())
                    grad.append(cur_grad)
                for (iop, op) in enumerate(grad[0]):
                    assert_almost_equal(grad[0][iop], grad[1][iop], rtol=rtol, atol=atol)
