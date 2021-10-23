@with_seed()
@use_np
def test_np_linalg_inv():

    class TestInverse(HybridBlock):

        def __init__(self):
            super(TestInverse, self).__init__()

        def hybrid_forward(self, F, data):
            return F.np.linalg.inv(data)

    def get_grad(A):
        if (0 in A.shape):
            return A
        dA = _np.ones_like(A)
        A_inv = _np.linalg.inv(A)
        dA_inv = (- _np.matmul(_np.matmul(A_inv, dA), A_inv))
        return _np.swapaxes(dA_inv, (- 1), (- 2))

    def check_inv(A_inv, data_np):
        assert (A_inv.shape == data_np.shape)
        try:
            A_expected = _np.linalg.inv(data_np)
        except Exception as e:
            print(data_np)
            print(data_np.shape)
            print(e)
        else:
            assert (A_inv.shape == A_expected.shape)
            assert_almost_equal(A_inv.asnumpy(), A_expected, rtol=rtol, atol=atol)
    shapes = [(0, 0), (4, 4), (2, 2), (1, 1), (2, 1, 1), (0, 1, 1), (6, 1, 1), (2, 3, 3, 3), (4, 2, 1, 1), (0, 5, 3, 3), (5, 0, 0, 0), (3, 3, 0, 0), (3, 5, 5)]
    dtypes = ['float32', 'float64']
    for (hybridize, dtype, shape) in itertools.product([True, False], dtypes, shapes):
        atol = rtol = 0.01
        test_inv = TestInverse()
        if hybridize:
            test_inv.hybridize()
        if (0 in shape):
            data_np = _np.ones(shape)
        else:
            n = shape[(- 1)]
            L = _np.tril(_np.random.uniform((- 10.0), 10.0, shape))
            U = _np.triu(_np.random.uniform((- 10.0), 10.0, shape))
            data_np = _np.matmul(L, U)
        data = np.array(data_np, dtype=dtype)
        data.attach_grad()
        with mx.autograd.record():
            A_inv = test_inv(data)
        check_inv(A_inv, data_np)
        mx.autograd.backward(A_inv)
        backward_expected = get_grad(data.asnumpy())
        assert_almost_equal(data.grad.asnumpy(), backward_expected, rtol=rtol, atol=atol)
        A_inv = np.linalg.inv(data)
        check_inv(A_inv, data_np)