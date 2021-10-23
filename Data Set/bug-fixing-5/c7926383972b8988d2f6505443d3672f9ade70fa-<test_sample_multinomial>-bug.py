@with_seed()
@unittest.skip('Flaky test: https://github.com/apache/incubator-mxnet/issues/11487')
def test_sample_multinomial():
    for dtype in ['uint8', 'int32', 'float16', 'float32', 'float64']:
        for x in [(mx.nd.array([[0, 1, 2, 3, 4], [4, 3, 2, 1, 0]]) / 10.0), (mx.nd.array([0, 1, 2, 3, 4]) / 10.0)]:
            dx = mx.nd.ones_like(x)
            mx.contrib.autograd.mark_variables([x], [dx])
            samples = 5000
            with mx.autograd.record():
                (y, prob) = mx.nd.random.multinomial(x, shape=samples, get_prob=True, dtype=dtype)
                r = (prob * 5)
                r.backward()
            assert (np.dtype(dtype) == y.dtype)
            y = y.asnumpy()
            x = x.asnumpy()
            dx = dx.asnumpy()
            if (len(x.shape) is 1):
                x = x.reshape((1, x.shape[0]))
                dx = dx.reshape(1, dx.shape[0])
                y = y.reshape((1, y.shape[0]))
                prob = prob.reshape((1, prob.shape[0]))
            for i in range(x.shape[0]):
                freq = ((np.bincount(y[i, :].astype('int32'), minlength=5) / np.float32(samples)) * x[i, :].sum())
                mx.test_utils.assert_almost_equal(freq, x[i], rtol=0.2)
                rprob = (x[i][y[i].astype('int32')] / x[i].sum())
                mx.test_utils.assert_almost_equal(np.log(rprob), prob.asnumpy()[i], atol=1e-05)
                real_dx = np.zeros((5,))
                for j in range(samples):
                    real_dx[int(y[i][j])] += (5.0 / rprob[j])
                mx.test_utils.assert_almost_equal(real_dx, dx[i, :], rtol=0.0001, atol=1e-05)
    for dtype in ['uint8', 'float16', 'float32']:
        x = mx.nd.zeros((2 ** 25))
        bound_check = False
        try:
            y = mx.nd.random.multinomial(x, dtype=dtype)
        except mx.MXNetError as e:
            bound_check = True
        assert bound_check