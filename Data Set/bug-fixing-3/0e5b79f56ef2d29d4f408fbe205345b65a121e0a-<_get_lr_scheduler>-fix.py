def _get_lr_scheduler(args, kv):
    if (('lr_factor' not in args) or (args.lr_factor >= 1)):
        return (args.lr, None)
    epoch_size = get_epoch_size(args, kv)
    begin_epoch = (args.load_epoch if args.load_epoch else 0)
    if ('pow' in args.lr_step_epochs):
        lr = args.lr
        max_up = (args.num_epochs * epoch_size)
        pwr = float(re.sub('pow[- ]*', '', args.lr_step_epochs))
        poly_sched = mx.lr_scheduler.PolyScheduler(max_up, lr, pwr)
        return (lr, poly_sched)
    step_epochs = [int(l) for l in args.lr_step_epochs.split(',')]
    lr = args.lr
    for s in step_epochs:
        if (begin_epoch >= s):
            lr *= args.lr_factor
    if (lr != args.lr):
        logging.info('Adjust learning rate to %e for epoch %d', lr, begin_epoch)
    steps = [(epoch_size * (x - begin_epoch)) for x in step_epochs if ((x - begin_epoch) > 0)]
    if steps:
        return (lr, mx.lr_scheduler.MultiFactorScheduler(step=steps, factor=args.lr_factor))
    else:
        return (lr, None)