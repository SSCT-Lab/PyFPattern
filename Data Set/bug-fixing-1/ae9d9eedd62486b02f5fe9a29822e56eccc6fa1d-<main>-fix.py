

def main():
    parser = argparse.ArgumentParser(description='Chainer CIFAR example:')
    parser.add_argument('--dataset', '-d', default='cifar10', help='The dataset to use: cifar10 or cifar100')
    parser.add_argument('--batchsize', '-b', type=int, default=64, help='Number of images in each mini-batch')
    parser.add_argument('--learnrate', '-l', type=float, default=0.05, help='Learning rate for SGD')
    parser.add_argument('--epoch', '-e', type=int, default=300, help='Number of sweeps over the dataset to train')
    parser.add_argument('--gpu', '-g', type=int, default=0, help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--out', '-o', default='result', help='Directory to output the result')
    parser.add_argument('--resume', '-r', default='', help='Resume the training from snapshot')
    parser.add_argument('--early-stopping', type=str, help='Metric to watch for early stopping')
    args = parser.parse_args()
    print('GPU: {}'.format(args.gpu))
    print('# Minibatch-size: {}'.format(args.batchsize))
    print('# epoch: {}'.format(args.epoch))
    print('')
    if (args.dataset == 'cifar10'):
        print('Using CIFAR10 dataset.')
        class_labels = 10
        (train, test) = get_cifar10()
    elif (args.dataset == 'cifar100'):
        print('Using CIFAR100 dataset.')
        class_labels = 100
        (train, test) = get_cifar100()
    else:
        raise RuntimeError('Invalid dataset choice.')
    model = L.Classifier(models.VGG.VGG(class_labels))
    if (args.gpu >= 0):
        chainer.backends.cuda.get_device_from_id(args.gpu).use()
        model.to_gpu()
    optimizer = chainer.optimizers.MomentumSGD(args.learnrate)
    optimizer.setup(model)
    optimizer.add_hook(chainer.optimizer_hooks.WeightDecay(0.0005))
    train_iter = chainer.iterators.SerialIterator(train, args.batchsize)
    test_iter = chainer.iterators.SerialIterator(test, args.batchsize, repeat=False, shuffle=False)
    stop_trigger = (args.epoch, 'epoch')
    if args.early_stopping:
        stop_trigger = triggers.EarlyStoppingTrigger(monitor=args.early_stopping, verbose=True, max_trigger=(args.epoch, 'epoch'))
    updater = training.updaters.StandardUpdater(train_iter, optimizer, device=args.gpu)
    trainer = training.Trainer(updater, stop_trigger, out=args.out)
    trainer.extend(extensions.Evaluator(test_iter, model, device=args.gpu))
    trainer.extend(extensions.ExponentialShift('lr', 0.5), trigger=(25, 'epoch'))
    trainer.extend(extensions.dump_graph('main/loss'))
    trainer.extend(extensions.snapshot(filename='snaphot_epoch_{.updater.epoch}'))
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'validation/main/loss', 'main/accuracy', 'validation/main/accuracy', 'elapsed_time']))
    trainer.extend(extensions.ProgressBar())
    if args.resume:
        chainer.serializers.load_npz(args.resume, trainer)
    trainer.run()
