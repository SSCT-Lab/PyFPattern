def train(net, train_data, val_data, eval_metric, batch_size, ctx, args):
    'Training pipeline'
    kv = mx.kvstore.create(('device' if (args.amp and ('nccl' in args.kv_store)) else args.kv_store))
    net.collect_params().setattr('grad_req', 'null')
    net.collect_train_params().setattr('grad_req', 'write')
    for (k, v) in net.collect_params('.*bias').items():
        v.wd_mult = 0.0
    optimizer_params = {
        'learning_rate': args.lr,
        'wd': args.wd,
        'momentum': args.momentum,
    }
    if args.horovod:
        hvd.broadcast_parameters(net.collect_params(), root_rank=0)
        trainer = hvd.DistributedTrainer(net.collect_train_params(), 'sgd', optimizer_params)
    else:
        trainer = gluon.Trainer(net.collect_train_params(), 'sgd', optimizer_params, update_on_kvstore=(False if args.amp else None), kvstore=kv)
    if args.amp:
        amp.init_trainer(trainer)
    lr_decay = float(args.lr_decay)
    lr_steps = sorted([float(ls) for ls in args.lr_decay_epoch.split(',') if ls.strip()])
    lr_warmup = float(args.lr_warmup)
    rpn_cls_loss = mx.gluon.loss.SigmoidBinaryCrossEntropyLoss(from_sigmoid=False)
    rpn_box_loss = mx.gluon.loss.HuberLoss(rho=(1 / 9.0))
    rcnn_cls_loss = mx.gluon.loss.SoftmaxCrossEntropyLoss()
    rcnn_box_loss = mx.gluon.loss.HuberLoss()
    rcnn_mask_loss = mx.gluon.loss.SigmoidBinaryCrossEntropyLoss(from_sigmoid=False)
    metrics = [mx.metric.Loss('RPN_Conf'), mx.metric.Loss('RPN_SmoothL1'), mx.metric.Loss('RCNN_CrossEntropy'), mx.metric.Loss('RCNN_SmoothL1'), mx.metric.Loss('RCNN_Mask')]
    rpn_acc_metric = RPNAccMetric()
    rpn_bbox_metric = RPNL1LossMetric()
    rcnn_acc_metric = RCNNAccMetric()
    rcnn_bbox_metric = RCNNL1LossMetric()
    rcnn_mask_metric = MaskAccMetric()
    rcnn_fgmask_metric = MaskFGAccMetric()
    metrics2 = [rpn_acc_metric, rpn_bbox_metric, rcnn_acc_metric, rcnn_bbox_metric, rcnn_mask_metric, rcnn_fgmask_metric]
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_file_path = (args.save_prefix + '_train.log')
    log_dir = os.path.dirname(log_file_path)
    if (log_dir and (not os.path.exists(log_dir))):
        os.makedirs(log_dir)
    fh = logging.FileHandler(log_file_path)
    logger.addHandler(fh)
    logger.info(args)
    if args.verbose:
        logger.info('Trainable parameters:')
        logger.info(net.collect_train_params().keys())
    logger.info('Start training from [Epoch {}]'.format(args.start_epoch))
    best_map = [0]
    for epoch in range(args.start_epoch, args.epochs):
        if (not args.disable_hybridization):
            net.hybridize(static_alloc=args.static_alloc)
        rcnn_task = ForwardBackwardTask(net, trainer, rpn_cls_loss, rpn_box_loss, rcnn_cls_loss, rcnn_box_loss, rcnn_mask_loss)
        executor = (Parallel(args.executor_threads, rcnn_task) if (not args.horovod) else None)
        while (lr_steps and (epoch >= lr_steps[0])):
            new_lr = (trainer.learning_rate * lr_decay)
            lr_steps.pop(0)
            trainer.set_learning_rate(new_lr)
            logger.info('[Epoch {}] Set learning rate to {}'.format(epoch, new_lr))
        for metric in metrics:
            metric.reset()
        tic = time.time()
        btic = time.time()
        base_lr = trainer.learning_rate
        for (i, batch) in enumerate(train_data):
            if ((epoch == 0) and (i <= lr_warmup)):
                new_lr = (base_lr * get_lr_at_iter((i / lr_warmup), args.lr_warmup_factor))
                if (new_lr != trainer.learning_rate):
                    if ((i % args.log_interval) == 0):
                        logger.info('[Epoch 0 Iteration {}] Set learning rate to {}'.format(i, new_lr))
                    trainer.set_learning_rate(new_lr)
            batch = split_and_load(batch, ctx_list=ctx)
            metric_losses = [[] for _ in metrics]
            add_losses = [[] for _ in metrics2]
            if (executor is not None):
                for data in zip(*batch):
                    executor.put(data)
            for j in range(len(ctx)):
                if (executor is not None):
                    result = executor.get()
                else:
                    result = rcnn_task.forward_backward(list(zip(*batch))[0])
                if ((not args.horovod) or (hvd.rank() == 0)):
                    for k in range(len(metric_losses)):
                        metric_losses[k].append(result[k])
                    for k in range(len(add_losses)):
                        add_losses[k].append(result[(len(metric_losses) + k)])
            for (metric, record) in zip(metrics, metric_losses):
                metric.update(0, record)
            for (metric, records) in zip(metrics2, add_losses):
                for pred in records:
                    metric.update(pred[0], pred[1])
            trainer.step(batch_size)
            if (((not args.horovod) or (hvd.rank() == 0)) and args.log_interval and (not ((i + 1) % args.log_interval))):
                msg = ','.join(['{}={:.3f}'.format(*metric.get()) for metric in (metrics + metrics2)])
                logger.info('[Epoch {}][Batch {}], Speed: {:.3f} samples/sec, {}'.format(epoch, i, ((args.log_interval * args.batch_size) / (time.time() - btic)), msg))
                btic = time.time()
        if ((not args.horovod) or (hvd.rank() == 0)):
            msg = ','.join(['{}={:.3f}'.format(*metric.get()) for metric in metrics])
            logger.info('[Epoch {}] Training cost: {:.3f}, {}'.format(epoch, (time.time() - tic), msg))
            if (not ((epoch + 1) % args.val_interval)):
                (map_name, mean_ap) = validate(net, val_data, ctx, eval_metric, args)
                val_msg = '\n'.join(['{}={}'.format(k, v) for (k, v) in zip(map_name, mean_ap)])
                logger.info('[Epoch {}] Validation: \n{}'.format(epoch, val_msg))
                current_map = float(mean_ap[(- 1)])
            else:
                current_map = 0.0
            save_params(net, logger, best_map, current_map, epoch, args.save_interval, args.save_prefix)