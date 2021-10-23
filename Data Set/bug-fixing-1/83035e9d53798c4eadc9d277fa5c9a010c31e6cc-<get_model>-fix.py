

def get_model(args, is_train, main_prog, startup_prog):
    (reader, dshape, class_dim) = _model_reader_dshape_classdim(args, is_train)
    pyreader = None
    trainer_count = int(os.getenv('PADDLE_TRAINERS'))
    with fluid.program_guard(main_prog, startup_prog):
        with fluid.unique_name.guard():
            if args.use_reader_op:
                pyreader = fluid.layers.py_reader(capacity=(args.batch_size * args.gpus), shapes=(([(- 1)] + dshape), ((- 1), 1)), dtypes=('float32', 'int64'), name=('train_reader' if is_train else 'test_reader'), use_double_buffer=True)
                (input, label) = fluid.layers.read_file(pyreader)
            else:
                input = fluid.layers.data(name='data', shape=dshape, dtype='float32')
                label = fluid.layers.data(name='label', shape=[1], dtype='int64')
            model = ResNet(is_train=is_train)
            predict = model.net(input, class_dim=class_dim)
            cost = fluid.layers.cross_entropy(input=predict, label=label)
            avg_cost = fluid.layers.mean(x=cost)
            batch_acc1 = fluid.layers.accuracy(input=predict, label=label, k=1)
            batch_acc5 = fluid.layers.accuracy(input=predict, label=label, k=5)
            optimizer = None
            if is_train:
                if args.use_lars:
                    lars_decay = 1.0
                else:
                    lars_decay = 0.0
                total_images = (1281167 / trainer_count)
                step = int(((total_images / (args.batch_size * args.gpus)) + 1))
                epochs = [30, 60, 90]
                bd = [(step * e) for e in epochs]
                base_lr = args.learning_rate
                lr = []
                lr = [(base_lr * (0.1 ** i)) for i in range((len(bd) + 1))]
                optimizer = fluid.optimizer.Momentum(learning_rate=fluid.layers.piecewise_decay(boundaries=bd, values=lr), momentum=0.9, regularization=fluid.regularizer.L2Decay(0.0001))
                optimizer.minimize(avg_cost)
                if args.memory_optimize:
                    fluid.memory_optimize(main_prog)
    if (not args.use_reader_op):
        batched_reader = paddle.batch((reader if args.no_random else paddle.reader.shuffle(reader, buf_size=5120)), batch_size=(args.batch_size * args.gpus), drop_last=True)
    else:
        batched_reader = None
        pyreader.decorate_paddle_reader(paddle.batch((reader if args.no_random else paddle.reader.shuffle(reader, buf_size=5120)), batch_size=args.batch_size))
    return (avg_cost, optimizer, [batch_acc1, batch_acc5], batched_reader, pyreader)
