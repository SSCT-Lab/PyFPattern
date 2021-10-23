

def main():
    archs = {
        'alex': alex.Alex,
        'alex_fp16': alex.AlexFp16,
        'googlenet': googlenet.GoogLeNet,
        'googlenetbn': googlenetbn.GoogLeNetBN,
        'googlenetbn_fp16': googlenetbn.GoogLeNetBNFp16,
        'nin': nin.NIN,
    }
    parser = argparse.ArgumentParser(description='Learning convnet from ILSVRC2012 dataset')
    parser.add_argument('train', help='Path to training image-label list file')
    parser.add_argument('val', help='Path to validation image-label list file')
    parser.add_argument('--arch', '-a', choices=archs.keys(), default='nin', help='Convnet architecture')
    parser.add_argument('--batchsize', '-B', type=int, default=32, help='Learning minibatch size')
    parser.add_argument('--epoch', '-E', type=int, default=10, help='Number of epochs to train')
    parser.add_argument('--gpus', '-g', type=int, nargs='*', default=[0, 1, 2, 3])
    parser.add_argument('--initmodel', help='Initialize the model from given file')
    parser.add_argument('--loaderjob', '-j', type=int, help='Number of parallel data loading processes')
    parser.add_argument('--mean', '-m', default='mean.npy', help='Mean file (computed by compute_mean.py)')
    parser.add_argument('--resume', '-r', default='', help='Initialize the trainer from given file')
    parser.add_argument('--out', '-o', default='result', help='Output directory')
    parser.add_argument('--root', '-R', default='.', help='Root directory path of image files')
    parser.add_argument('--val_batchsize', '-b', type=int, default=250, help='Validation minibatch size')
    parser.add_argument('--test', action='store_true')
    parser.set_defaults(test=False)
    args = parser.parse_args()
    model = archs[args.arch]()
    if args.initmodel:
        print('Load model from', args.initmodel)
        chainer.serializers.load_npz(args.initmodel, model)
    mean = np.load(args.mean)
    train = train_imagenet.PreprocessedDataset(args.train, args.root, mean, model.insize)
    val = train_imagenet.PreprocessedDataset(args.val, args.root, mean, model.insize, False)
    devices = tuple(args.gpus)
    train_iters = [chainer.iterators.MultiprocessIterator(i, args.batchsize, n_processes=args.loaderjob) for i in chainer.datasets.split_dataset_n_random(train, len(devices))]
    val_iter = chainer.iterators.MultiprocessIterator(val, args.val_batchsize, repeat=False, n_processes=args.loaderjob)
    optimizer = chainer.optimizers.MomentumSGD(lr=0.01, momentum=0.9)
    optimizer.setup(model)
    updater = updaters.MultiprocessParallelUpdater(train_iters, optimizer, devices=devices)
    trainer = training.Trainer(updater, (args.epoch, 'epoch'), args.out)
    if args.test:
        val_interval = (5, 'epoch')
        log_interval = (1, 'epoch')
    else:
        val_interval = (100000, 'iteration')
        log_interval = (1000, 'iteration')
    trainer.extend(train_imagenet.TestModeEvaluator(val_iter, model, device=args.gpus[0]), trigger=val_interval)
    trainer.extend(extensions.dump_graph('main/loss'))
    trainer.extend(extensions.snapshot(), trigger=val_interval)
    trainer.extend(extensions.snapshot_object(model, 'model_iter_{.updater.iteration}'), trigger=val_interval)
    trainer.extend(extensions.LogReport(trigger=log_interval))
    trainer.extend(extensions.observe_lr(), trigger=log_interval)
    trainer.extend(extensions.PrintReport(['epoch', 'iteration', 'main/loss', 'validation/main/loss', 'main/accuracy', 'validation/main/accuracy', 'lr']), trigger=log_interval)
    trainer.extend(extensions.ProgressBar(update_interval=2))
    if args.resume:
        chainer.serializers.load_npz(args.resume, trainer)
    trainer.run()
