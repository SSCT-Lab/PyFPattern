def main():
    parser = argparse.ArgumentParser(description='Chainer example: MNIST')
    parser.add_argument('--batchsize', '-b', type=int, default=100, help='Number of images in each mini-batch')
    parser.add_argument('--epoch', '-e', type=int, default=20, help='Number of sweeps over the dataset to train')
    parser.add_argument('--gpu', '-g', type=int, default=(- 1), help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--out', '-o', default='result', help='Directory to output the result')
    parser.add_argument('--resume', '-r', default='', help='Resume the training from snapshot using model and state files in the specified directory')
    parser.add_argument('--unit', '-u', type=int, default=1000, help='Number of units')
    args = parser.parse_args()
    print('GPU: {}'.format(args.gpu))
    print('# unit: {}'.format(args.unit))
    print('# Minibatch-size: {}'.format(args.batchsize))
    print('# epoch: {}'.format(args.epoch))
    print('')
    model = L.Classifier(train_mnist.MLP(args.unit, 10))
    if (args.gpu >= 0):
        chainer.backends.cuda.get_device_from_id(args.gpu).use()
        model.to_gpu()
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)
    if args.resume:
        serializers.load_npz('{}/mlp.model'.format(args.resume), model)
        serializers.load_npz('{}/mlp.state'.format(args.resume), optimizer)
    (train, test) = chainer.datasets.get_mnist()
    train_count = len(train)
    test_count = len(test)
    train_iter = chainer.iterators.SerialIterator(train, args.batchsize)
    test_iter = chainer.iterators.SerialIterator(test, args.batchsize, repeat=False, shuffle=False)
    sum_accuracy = 0
    sum_loss = 0
    while (train_iter.epoch < args.epoch):
        batch = train_iter.next()
        (x, t) = convert.concat_examples(batch, args.gpu)
        optimizer.update(model, x, t)
        sum_loss += (float(model.loss.data) * len(t))
        sum_accuracy += (float(model.accuracy.data) * len(t))
        if train_iter.is_new_epoch:
            print('epoch: {}'.format(train_iter.epoch))
            print('train mean loss: {}, accuracy: {}'.format((sum_loss / train_count), (sum_accuracy / train_count)))
            sum_accuracy = 0
            sum_loss = 0
            with configuration.using_config('train', False):
                with chainer.using_config('enable_backprop', False):
                    for batch in test_iter:
                        (x, t) = convert.concat_examples(batch, args.gpu)
                        loss = model(x, t)
                        sum_loss += (float(loss.data) * len(t))
                        sum_accuracy += (float(model.accuracy.data) * len(t))
            test_iter.reset()
            print('test mean  loss: {}, accuracy: {}'.format((sum_loss / test_count), (sum_accuracy / test_count)))
            sum_accuracy = 0
            sum_loss = 0
    print('save the model')
    serializers.save_npz('{}/mlp.model'.format(args.out), model)
    print('save the optimizer')
    serializers.save_npz('{}/mlp.state'.format(args.out), optimizer)