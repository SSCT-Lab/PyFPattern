

@with_seed(1234)
def test_bce_loss():
    N = 20
    data = mx.random.uniform((- 1), 1, shape=(N, 20))
    label = mx.nd.array(np.random.randint(2, size=(N,)), dtype='float32')
    data_iter = mx.io.NDArrayIter(data, label, batch_size=10, label_name='label')
    output = get_net(1)
    l = mx.symbol.Variable('label')
    Loss = gluon.loss.SigmoidBinaryCrossEntropyLoss()
    loss = Loss(output, l)
    loss = mx.sym.make_loss(loss)
    mod = mx.mod.Module(loss, data_names=('data',), label_names=('label',))
    mod.fit(data_iter, num_epoch=200, optimizer_params={
        'learning_rate': 0.01,
    }, eval_metric=mx.metric.Loss(), optimizer='adam', initializer=mx.init.Xavier(magnitude=2))
    assert (mod.score(data_iter, eval_metric=mx.metric.Loss())[0][1] < 0.01)
    data = mx.random.uniform((- 5), 5, shape=(10,))
    label = mx.random.uniform(0, 1, shape=(10,))
    mx_bce_loss = Loss(data, label).asnumpy()
    prob_npy = (1.0 / (1.0 + np.exp((- data.asnumpy()))))
    label_npy = label.asnumpy()
    npy_bce_loss = (((- label_npy) * np.log(prob_npy)) - ((1 - label_npy) * np.log((1 - prob_npy))))
    assert_almost_equal(mx_bce_loss, npy_bce_loss)
