

def train(net, train_data, val_data, eval_metric, ctx, args):
    'Training pipeline'
    net.collect_params().reset_ctx(ctx)
    if args.no_wd:
        for (k, v) in net.collect_params('.*beta|.*gamma|.*bias').items():
            v.wd_mult = 0.0
    if args.label_smooth:
        net._target_generator._label_smooth = True
    if (args.lr_decay_period > 0):
        lr_decay_epoch = list(range(lr_decay_period, args.epochs, lr_decay_period))
    else:
        lr_decay_epoch = [int(i) for i in args.lr_decay_epoch.split(',')]
    lr_scheduler = LRScheduler(mode=args.lr_mode, baselr=args.lr, niters=(args.num_samples // args.batch_size), nepochs=args.epochs, step=lr_decay_epoch, step_factor=args.lr_decay, power=2, warmup_epochs=args.warmup_epochs)
    trainer = gluon.Trainer(net.collect_params(), 'sgd', {
        'wd': args.wd,
        'momentum': args.momentum,
        'lr_scheduler': lr_scheduler,
    }, kvstore='local')
    sigmoid_ce = gluon.loss.SigmoidBinaryCrossEntropyLoss(from_sigmoid=False)
    l1_loss = gluon.loss.L1Loss()
    obj_metrics = mx.metric.Loss('ObjLoss')
    center_metrics = mx.metric.Loss('BoxCenterLoss')
    scale_metrics = mx.metric.Loss('BoxScaleLoss')
    cls_metrics = mx.metric.Loss('ClassLoss')
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
    logger.info('Start training from [Epoch {}]'.format(args.start_epoch))
    best_map = [0]
    for epoch in range(args.start_epoch, args.epochs):
        if args.mixup:
            try:
                train_data._dataset.set_mixup(np.random.beta, 1.5, 1.5)
            except AttributeError:
                train_data._dataset._data.set_mixup(np.random.beta, 1.5, 1.5)
            if (epoch >= (args.epochs - args.no_mixup_epochs)):
                try:
                    train_data._dataset.set_mixup(None)
                except AttributeError:
                    train_data._dataset._data.set_mixup(None)
        tic = time.time()
        btic = time.time()
        mx.nd.waitall()
        net.hybridize()
        for (i, batch) in enumerate(train_data):
            batch_size = batch[0].shape[0]
            data = gluon.utils.split_and_load(batch[0], ctx_list=ctx, batch_axis=0)
            fixed_targets = [gluon.utils.split_and_load(batch[it], ctx_list=ctx, batch_axis=0) for it in range(1, 6)]
            gt_boxes = gluon.utils.split_and_load(batch[6], ctx_list=ctx, batch_axis=0)
            sum_losses = []
            obj_losses = []
            center_losses = []
            scale_losses = []
            cls_losses = []
            with autograd.record():
                for (ix, x) in enumerate(data):
                    (obj_loss, center_loss, scale_loss, cls_loss) = net(x, gt_boxes[ix], *[ft[ix] for ft in fixed_targets])
                    sum_losses.append((((obj_loss + center_loss) + scale_loss) + cls_loss))
                    obj_losses.append(obj_loss)
                    center_losses.append(center_loss)
                    scale_losses.append(scale_loss)
                    cls_losses.append(cls_loss)
                autograd.backward(sum_losses)
            lr_scheduler.update(i, epoch)
            trainer.step(batch_size)
            obj_metrics.update(0, obj_losses)
            center_metrics.update(0, center_losses)
            scale_metrics.update(0, scale_losses)
            cls_metrics.update(0, cls_losses)
            if (args.log_interval and (not ((i + 1) % args.log_interval))):
                (name1, loss1) = obj_metrics.get()
                (name2, loss2) = center_metrics.get()
                (name3, loss3) = scale_metrics.get()
                (name4, loss4) = cls_metrics.get()
                logger.info('[Epoch {}][Batch {}], LR: {:.2E}, Speed: {:.3f} samples/sec, {}={:.3f}, {}={:.3f}, {}={:.3f}, {}={:.3f}'.format(epoch, i, trainer.learning_rate, (batch_size / (time.time() - btic)), name1, loss1, name2, loss2, name3, loss3, name4, loss4))
            btic = time.time()
        (name1, loss1) = obj_metrics.get()
        (name2, loss2) = center_metrics.get()
        (name3, loss3) = scale_metrics.get()
        (name4, loss4) = cls_metrics.get()
        logger.info('[Epoch {}] Training cost: {:.3f}, {}={:.3f}, {}={:.3f}, {}={:.3f}, {}={:.3f}'.format(epoch, (time.time() - tic), name1, loss1, name2, loss2, name3, loss3, name4, loss4))
        if (not ((epoch + 1) % args.val_interval)):
            (map_name, mean_ap) = validate(net, val_data, ctx, eval_metric)
            val_msg = '\n'.join(['{}={}'.format(k, v) for (k, v) in zip(map_name, mean_ap)])
            logger.info('[Epoch {}] Validation: \n{}'.format(epoch, val_msg))
            current_map = float(mean_ap[(- 1)])
        else:
            current_map = 0.0
        save_params(net, best_map, current_map, epoch, args.save_interval, args.save_prefix)
