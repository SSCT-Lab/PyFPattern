

@unittest.skip('flaky test. https://github.com/apache/incubator-mxnet/issues/8892')
@with_seed(1234)
def test_ctc_loss_train():
    N = 20
    data = mx.random.uniform((- 1), 1, shape=(N, 20, 10))
    label = mx.nd.arange(4, repeat=N).reshape((N, 4))
    data_iter = mx.io.NDArrayIter(data, label, batch_size=10, label_name='label', shuffle=True)
    output = get_net(5, False)
    l = mx.symbol.Variable('label')
    Loss = gluon.loss.CTCLoss(layout='NTC', label_layout='NT')
    loss = Loss(output, l)
    loss = mx.sym.make_loss(loss)
    mod = mx.mod.Module(loss, data_names=('data',), label_names=('label',))
    mod.fit(data_iter, num_epoch=200, optimizer_params={
        'learning_rate': 1.0,
    }, initializer=mx.init.Xavier(magnitude=2), eval_metric=mx.metric.Loss(), optimizer='adam')
    assert (mod.score(data_iter, eval_metric=mx.metric.Loss())[0][1] < 10)
