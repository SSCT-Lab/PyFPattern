def test_l2_loss():
    np.random.seed(1234)
    N = 20
    data = mx.random.uniform((- 1), 1, shape=(N, 10))
    label = mx.random.uniform((- 1), 1, shape=(N, 1))
    data_iter = mx.io.NDArrayIter(data, label, batch_size=10, label_name='label', shuffle=True)
    output = get_net(1)
    l = mx.symbol.Variable('label')
    Loss = gluon.loss.L2Loss()
    Loss(label, label)
    loss = Loss(output, l)
    loss = mx.sym.make_loss(loss)
    mod = mx.mod.Module(loss, data_names=('data',), label_names=('label',))
    mod.fit(data_iter, num_epoch=200, optimizer_params={
        'learning_rate': 0.1,
        'wd': 0.00045,
    }, initializer=mx.init.Xavier(magnitude=2), eval_metric=mx.metric.Loss())
    assert (mod.score(data_iter, eval_metric=mx.metric.Loss())[0][1] < 0.05)