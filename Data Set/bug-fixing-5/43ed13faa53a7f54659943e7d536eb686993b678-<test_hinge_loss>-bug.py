@with_seed(1234)
def test_hinge_loss():
    N = 20
    data = mx.random.uniform((- 1), 1, shape=(N, 10))
    label = mx.nd.sign(mx.random.uniform((- 1), 1, shape=(N, 1)))
    data_iter = mx.io.NDArrayIter(data, label, batch_size=10, label_name='label', shuffle=True)
    output = get_net(1)
    l = mx.symbol.Variable('label')
    Loss = gluon.loss.HingeLoss()
    loss = Loss(output, l)
    loss = mx.sym.make_loss(loss)
    mod = mx.mod.Module(loss, data_names=('data',), label_names=('label',))
    mod.fit(data_iter, num_epoch=200, optimizer_params={
        'learning_rate': 0.01,
    }, initializer=mx.init.Xavier(magnitude=2), eval_metric=mx.metric.Loss(), optimizer='adam')
    assert (mod.score(data_iter, eval_metric=mx.metric.Loss())[0][1] < 0.05)