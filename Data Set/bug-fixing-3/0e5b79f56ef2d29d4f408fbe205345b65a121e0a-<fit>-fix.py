def fit(args, network, data_loader, **kwargs):
    '\n    train a model\n    args : argparse returns\n    network : the symbol definition of the nerual network\n    data_loader : function that returns the train and val data iterators\n    '
    kv = mx.kvstore.create(args.kv_store)
    if (args.gc_type != 'none'):
        kv.set_gradient_compression({
            'type': args.gc_type,
            'threshold': args.gc_threshold,
        })
    head = (('%(asctime)-15s Node[' + str(kv.rank)) + '] %(message)s')
    logging.basicConfig(level=logging.DEBUG, format=head)
    logging.info('start with arguments %s', args)
    epoch_size = get_epoch_size(args, kv)
    (train, val) = data_loader(args, kv)
    if (('dist' in args.kv_store) and (not ('async' in args.kv_store))):
        logging.info('Resizing training data to %d batches per machine', epoch_size)
        train = mx.io.ResizeIter(train, epoch_size)
    if args.test_io:
        tic = time.time()
        for (i, batch) in enumerate(train):
            for j in batch.data:
                j.wait_to_read()
            if (((i + 1) % args.disp_batches) == 0):
                logging.info('Batch [%d]\tSpeed: %.2f samples/sec', i, ((args.disp_batches * args.batch_size) / (time.time() - tic)))
                tic = time.time()
        return
    if (('arg_params' in kwargs) and ('aux_params' in kwargs)):
        arg_params = kwargs['arg_params']
        aux_params = kwargs['aux_params']
    else:
        (sym, arg_params, aux_params) = _load_model(args, kv.rank)
        if (sym is not None):
            assert (sym.tojson() == network.tojson())
    checkpoint = _save_model(args, kv.rank)
    devs = (mx.cpu() if ((args.gpus is None) or (args.gpus == '')) else [mx.gpu(int(i)) for i in args.gpus.split(',')])
    (lr, lr_scheduler) = _get_lr_scheduler(args, kv)
    model = mx.mod.Module(context=devs, symbol=network)
    lr_scheduler = lr_scheduler
    optimizer_params = {
        'learning_rate': lr,
        'wd': args.wd,
        'lr_scheduler': lr_scheduler,
        'multi_precision': True,
    }
    has_momentum = {'sgd', 'dcasgd', 'nag'}
    if (args.optimizer in has_momentum):
        optimizer_params['momentum'] = args.mom
    monitor = (mx.mon.Monitor(args.monitor, pattern='.*') if (args.monitor > 0) else None)
    has_warmup = {'lbsgd', 'lbnag'}
    if (args.optimizer in has_warmup):
        nworkers = kv.num_workers
        if (epoch_size < 1):
            epoch_size = 1
        macrobatch_size = args.macrobatch_size
        if (macrobatch_size < (args.batch_size * nworkers)):
            macrobatch_size = (args.batch_size * nworkers)
        batch_scale = math.ceil(((float(macrobatch_size) / args.batch_size) / nworkers))
        optimizer_params['updates_per_epoch'] = epoch_size
        optimizer_params['begin_epoch'] = (args.load_epoch if args.load_epoch else 0)
        optimizer_params['batch_scale'] = batch_scale
        optimizer_params['warmup_strategy'] = args.warmup_strategy
        optimizer_params['warmup_epochs'] = args.warmup_epochs
        optimizer_params['num_epochs'] = args.num_epochs
    if (args.initializer == 'default'):
        if (args.network == 'alexnet'):
            initializer = mx.init.Normal()
        elif (args.network and ('vgg' in args.network)):
            initializer = mx.init.Xavier()
        else:
            initializer = mx.init.Xavier(rnd_type='gaussian', factor_type='in', magnitude=2)
    elif (args.initializer == 'xavier'):
        initializer = mx.init.Xavier()
    elif (args.initializer == 'msra'):
        initializer = mx.init.MSRAPrelu()
    elif (args.initializer == 'orthogonal'):
        initializer = mx.init.Orthogonal()
    elif (args.initializer == 'normal'):
        initializer = mx.init.Normal()
    elif (args.initializer == 'uniform'):
        initializer = mx.init.Uniform()
    elif (args.initializer == 'one'):
        initializer = mx.init.One()
    elif (args.initializer == 'zero'):
        initializer = mx.init.Zero()
    eval_metrics = ['accuracy']
    if (args.top_k > 0):
        eval_metrics.append(mx.metric.create('top_k_accuracy', top_k=args.top_k))
    supported_loss = ['ce', 'nll_loss']
    if (len(args.loss) > 0):
        loss_type_list = args.loss.split(',')
        if ('softmax_output' in network.list_outputs()):
            for loss_type in loss_type_list:
                loss_type = loss_type.strip()
                if (loss_type == 'nll'):
                    loss_type = 'nll_loss'
                if (loss_type not in supported_loss):
                    logging.warning((loss_type + ' is not an valid loss type, only cross-entropy or negative likelihood loss is supported!'))
                else:
                    eval_metrics.append(mx.metric.create(loss_type))
        else:
            logging.warning('The output is not softmax_output, loss argument will be skipped!')
    batch_end_callbacks = [mx.callback.Speedometer(args.batch_size, args.disp_batches)]
    if ('batch_end_callback' in kwargs):
        cbs = kwargs['batch_end_callback']
        batch_end_callbacks += (cbs if isinstance(cbs, list) else [cbs])
    model.fit(train, begin_epoch=(args.load_epoch if args.load_epoch else 0), num_epoch=args.num_epochs, eval_data=val, eval_metric=eval_metrics, kvstore=kv, optimizer=args.optimizer, optimizer_params=optimizer_params, initializer=initializer, arg_params=arg_params, aux_params=aux_params, batch_end_callback=batch_end_callbacks, epoch_end_callback=checkpoint, allow_missing=True, monitor=monitor)