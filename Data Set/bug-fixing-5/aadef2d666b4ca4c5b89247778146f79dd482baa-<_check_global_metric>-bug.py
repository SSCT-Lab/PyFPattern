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
    assert (m1.get() == m2.get())