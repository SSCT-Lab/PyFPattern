

@with_seed()
def test_ce_loss():
    nclass = 10
    N = 20
    data = mx.random.uniform((- 1), 1, shape=(N, nclass))
    label = mx.nd.array(np.random.randint(0, nclass, size=(N,)), dtype='int32')
    data_iter = mx.io.NDArrayIter(data, label, batch_size=10, label_name='label')
    output = get_net(nclass)
    l = mx.symbol.Variable('label')
    Loss = gluon.loss.SoftmaxCrossEntropyLoss()
    loss = Loss(output, l)
    loss = mx.sym.make_loss(loss)
    mod = mx.mod.Module(loss, data_names=('data',), label_names=('label',))
    mod.fit(data_iter, num_epoch=200, optimizer_params={
        'learning_rate': 0.01,
    }, eval_metric=mx.metric.Loss(), optimizer='adam', initializer=mx.init.Xavier(magnitude=2))
    assert (mod.score(data_iter, eval_metric=mx.metric.Loss())[0][1] < 0.05)
