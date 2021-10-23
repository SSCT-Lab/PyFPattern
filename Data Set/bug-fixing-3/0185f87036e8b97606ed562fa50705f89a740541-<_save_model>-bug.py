def _save_model(args, rank=0):
    if (args.model_prefix is None):
        return None
    dst_dir = os.path.dirname(args.model_prefix)
    if (not os.path.isdir(dst_dir)):
        os.mkdir(dst_dir)
    return mx.callback.do_checkpoint((args.model_prefix if (rank == 0) else ('%s-%d' % (args.model_prefix, rank))))