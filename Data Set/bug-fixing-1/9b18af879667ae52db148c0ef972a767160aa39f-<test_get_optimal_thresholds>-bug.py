

@with_seed()
@unittest.skip('Flaky test: https://github.com/apache/incubator-mxnet/issues/11456')
def test_get_optimal_thresholds():

    def get_threshold(nd):
        min_nd = mx.nd.min(nd)
        max_nd = mx.nd.max(nd)
        return mx.nd.maximum(mx.nd.abs(min_nd), mx.nd.abs(max_nd)).asnumpy()
    nd_dict = {
        'layer1': mx.nd.uniform(low=(- 10.532), high=11.3432, shape=(8, 3, 23, 23)),
    }
    expected_threshold = get_threshold(nd_dict['layer1'])
    th_dict = mx.contrib.quant._get_optimal_thresholds(nd_dict)
    assert ('layer1' in th_dict)
    assert_almost_equal(np.array([th_dict['layer1'][1]]), expected_threshold, rtol=0.001, atol=0.001)
