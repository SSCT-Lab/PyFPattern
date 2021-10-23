def test_sample_weight_loss():
    np.random.seed(1234)
    nclass = 10
    N = 20
    data = mx.random.uniform((- 1), 1, shape=(N, nclass))
    label = mx.nd.array(np.random.randint(0, nclass, size=(N,)), dtype='int32')
    weight = mx.nd.array(([1 for i in range(10)] + [0 for i in range(10)]))
    data_iter = mx.io.NDArrayIter(data, {
        'label': label,
        'w': weight,
    }, batch_size=10)
    output = get_net(nclass)
    l = mx.symbol.Variable('label')
    w = mx.symbol.Variable('w')
    Loss = gluon.loss.SoftmaxCrossEntropyLoss()
    loss = Loss(output, l, w)
    loss = mx.sym.make_loss(loss)
    mod = mx.mod.Module(loss, data_names=('data',), label_names=('label', 'w'))
    mod.fit(data_iter, num_epoch=200, optimizer_params={
        'learning_rate': 1.0,
    }, eval_metric=mx.metric.Loss())
    data_iter = mx.io.NDArrayIter(data[10:], {
        'label': label,
        'w': weight,
    }, batch_size=10)
    score = mod.score(data_iter, eval_metric=mx.metric.Loss())[0][1]
    assert (score > 1)
    data_iter = mx.io.NDArrayIter(data[:10], {
        'label': label,
        'w': weight,
    }, batch_size=10)
    score = mod.score(data_iter, eval_metric=mx.metric.Loss())[0][1]
    assert (score < 0.05)