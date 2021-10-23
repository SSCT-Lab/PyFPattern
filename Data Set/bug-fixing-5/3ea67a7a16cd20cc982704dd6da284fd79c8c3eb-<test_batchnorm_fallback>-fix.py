@with_seed()
def test_batchnorm_fallback():
    stype = 'row_sparse'
    for shape in [(2, 3), (2, 3, 2, 2)]:
        data_tmp = np.random.normal((- 0.1), 0.1, size=shape)
        s = (shape[1],)
        gamma = np.ones(s)
        beta = np.ones(s)
        gamma[1] = 3
        beta[0] = 3
        rolling_mean = np.random.uniform(size=s)
        rolling_std = np.random.uniform(size=s)
        data = mx.symbol.Variable('data', stype=stype)
        in_location = [mx.nd.array(data_tmp).tostype(stype), mx.nd.array(gamma).tostype(stype), mx.nd.array(beta).tostype(stype)]
        mean_std = [mx.nd.array(rolling_mean).tostype(stype), mx.nd.array(rolling_std).tostype(stype)]
        test = mx.symbol.BatchNorm(data, fix_gamma=True)
        assertRaises(MXNetError, check_numeric_gradient, test, in_location, mean_std, numeric_eps=0.001, rtol=0.16, atol=0.01)
        test = mx.symbol.BatchNorm(data, fix_gamma=True, use_global_stats=True)
        assertRaises(MXNetError, check_numeric_gradient, test, in_location, mean_std, numeric_eps=0.001, rtol=0.16, atol=0.01)
        test = mx.symbol.BatchNorm(data, fix_gamma=False)
        check_numeric_gradient(test, in_location, mean_std, numeric_eps=0.001, rtol=0.16, atol=0.01)
        test = mx.symbol.BatchNorm(data, fix_gamma=False, use_global_stats=True)
        check_numeric_gradient(test, in_location, mean_std, numeric_eps=0.001, rtol=0.16, atol=0.01)
        dim = len(shape)
        for chaxis in range((- dim), dim):
            chaxis_true = chaxis
            if (chaxis < 0):
                chaxis_true = (dim + chaxis)
            shapex = shape
            channel_count = shapex[chaxis_true]
            data_tmp = np.random.normal((- 0.1), 0.1, size=shapex)
            gamma = np.ones(channel_count)
            beta = np.ones(channel_count)
            if (channel_count > 1):
                gamma[1] = 3
            beta[0] = 3
            in_location = [mx.nd.array(data_tmp).tostype(stype), mx.nd.array(gamma).tostype(stype), mx.nd.array(beta).tostype(stype)]
            xrolling_mean = np.random.uniform(size=channel_count)
            xrolling_std = np.random.uniform(size=channel_count)
            xmean_std = [mx.nd.array(xrolling_mean).tostype(stype), mx.nd.array(xrolling_std).tostype(stype)]
            test = mx.symbol.BatchNorm(data, fix_gamma=True, axis=chaxis)
            assertRaises(MXNetError, check_numeric_gradient, test, in_location, xmean_std, numeric_eps=0.001, rtol=0.2, atol=0.01)
            test = mx.symbol.BatchNorm(data, fix_gamma=True, use_global_stats=True, axis=chaxis)
            assertRaises(MXNetError, check_numeric_gradient, test, in_location, xmean_std, numeric_eps=0.001, rtol=0.2, atol=0.01)
            test = mx.symbol.BatchNorm(data, fix_gamma=False, axis=chaxis)
            check_numeric_gradient(test, in_location, xmean_std, numeric_eps=0.001, rtol=0.2, atol=0.01)
            test = mx.symbol.BatchNorm(data, fix_gamma=False, use_global_stats=True, axis=chaxis)
            check_numeric_gradient(test, in_location, xmean_std, numeric_eps=0.001, rtol=0.2, atol=0.01)