def _save_model(args, rank=0):
    if (args.model_prefix is None):
        return None
    return mx.callback.do_checkpoint((args.model_prefix if (rank == 0) else ('%s-%d' % (args.model_prefix, rank))), period=args.save_period)