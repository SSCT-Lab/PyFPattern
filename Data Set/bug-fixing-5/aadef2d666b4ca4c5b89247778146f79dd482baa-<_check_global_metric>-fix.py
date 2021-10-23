def _check_global_metric(metric, *args, **kwargs):

    def _create_pred_label():
        if use_same_shape:
            pred = mx.nd.random.uniform(0, 1, shape=shape)
            label = mx.nd.random.uniform(0, 1, shape=shape)
        else:
            idx = np.random.rand(*shape).argsort(1)
            pred = mx.nd.array((1 - (0.1 * idx)))
            label = mx.nd.ones(shape[0])
            label[:(shape[0] // 2)] = 0
        return (pred, label)

    def _compare_metric_result(m1, m2):
        assert (m1[0] == m2[0])
        if isinstance(m1[1], (list, tuple)):
            assert (len(m1[1]) == len(m2[1]))
            for (r1, r2) in zip(m1[1], m2[1]):
                assert ((r1 == r2) or (math.isnan(r1) and math.isnan(r2)))
        else:
            assert ((m1[1] == m2[1]) or (math.isnan(m1[1]) and math.isnan(m2[1])))
    shape = kwargs.pop('shape', (10, 10))
    use_same_shape = kwargs.pop('use_same_shape', False)
    m1 = mx.metric.create(metric, *args, **kwargs)
    m2 = deepcopy(m1)
    for i in range(10):
        (pred, label) = _create_pred_label()
        m1.update([label], [pred])
        m1.reset_local()
        m2.update([label], [pred])
    assert (m1.get_global() == m2.get())
    m1.reset_local()
    m2.reset()
    (pred, label) = _create_pred_label()
    m1.update([label], [pred])
    m1.reset_local()
    (pred, label) = _create_pred_label()
    m1.update([label], [pred])
    m2.update([label], [pred])
    _compare_metric_result(m1.get(), m2.get())