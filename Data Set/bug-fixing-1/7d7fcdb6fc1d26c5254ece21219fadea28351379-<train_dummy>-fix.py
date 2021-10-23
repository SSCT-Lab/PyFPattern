

def train_dummy(ctx):
    if isinstance(ctx, mx.Context):
        ctx = [ctx]
    net.initialize(mx.init.Xavier(magnitude=2), ctx=ctx)
    data = []
    label = []
    bs = (batch_size // len(ctx))
    for c in ctx:
        data.append(mx.nd.random.uniform(shape=(bs, 3, 224, 224), ctx=c))
        label.append(mx.nd.ones(shape=bs, ctx=c))
    trainer = gluon.Trainer(net.collect_params(), optimizer, optimizer_params)
    L = gluon.loss.SoftmaxCrossEntropyLoss()
    acc_top1.reset()
    acc_top5.reset()
    btic = time.time()
    train_loss = 0
    num_batch = 1000
    warm_up = 100
    for i in range(num_batch):
        if (i == warm_up):
            tic = time.time()
        if opt.label_smoothing:
            label_smooth = smooth(label)
        else:
            label_smooth = label
        with ag.record():
            outputs = [net(X) for X in data]
            loss = [L(yhat, y) for (yhat, y) in zip(outputs, label_smooth)]
        for l in loss:
            l.backward()
        trainer.step(batch_size)
        acc_top1.update(label, outputs)
        acc_top5.update(label, outputs)
        train_loss += sum([l.sum().asscalar() for l in loss])
        if (opt.log_interval and (not ((i + 1) % opt.log_interval))):
            logging.info(('Batch [%d]\tSpeed: %f samples/sec' % (i, ((batch_size * opt.log_interval) / (time.time() - btic)))))
            btic = time.time()
    total_time_cost = (time.time() - tic)
    logging.info(('Test finished. Average Speed: %f samples/sec. Total time cost: %f' % (((batch_size * (num_batch - warm_up)) / total_time_cost), total_time_cost)))
