def test_kl_loss():
    np.random.seed(1234)
    N = 20
    data = mx.random.uniform((- 1), 1, shape=(N, 10))
    label = mx.nd.softmax(mx.random.uniform(0, 1, shape=(N, 2)))
    data_iter = mx.io.NDArrayIter(data, label, batch_size=10, label_name='label')
    output = mx.sym.log_softmax(get_net(2))
    l = mx.symbol.Variable('label')
    Loss = gluon.loss.KLDivLoss()
    loss = Loss(output, l)
    loss = mx.sym.make_loss(loss)
    mod = mx.mod.Module(loss, data_names=('data',), label_names=('label',))
    mod.fit(data_iter, num_epoch=200, optimizer_params={
        'learning_rate': 1.0,
    }, eval_metric=mx.metric.Loss())
    assert (mod.score(data_iter, eval_metric=mx.metric.Loss())[0][1] < 0.05)