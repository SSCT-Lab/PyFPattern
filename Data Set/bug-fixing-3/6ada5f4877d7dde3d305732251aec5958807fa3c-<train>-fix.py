def train(avg_loss, infer_prog, optimizer, train_reader, test_reader, batch_acc, args, train_prog, startup_prog):
    if (os.getenv('PADDLE_TRAINING_ROLE') == 'PSERVER'):
        place = core.CPUPlace()
        exe = fluid.Executor(place)
        exe.run(startup_prog)
        exe.run(train_prog)
        return
    if args.use_fake_data:
        raise Exception('fake data is not supported in single GPU test for now.')
    place = (core.CPUPlace() if (args.device == 'CPU') else core.CUDAPlace(0))
    exe = fluid.Executor(place)
    exe.run(startup_prog)
    feed_var_list = [var for var in train_prog.global_block().vars.itervalues() if var.is_data]
    feeder = fluid.DataFeeder(feed_var_list, place)
    (iters, num_samples, start_time) = (0, 0, time.time())
    for pass_id in range(args.pass_num):
        train_losses = []
        for (batch_id, data) in enumerate(train_reader()):
            if (iters == args.skip_batch_num):
                start_time = time.time()
                num_samples = 0
            if (iters == args.iterations):
                break
            loss = exe.run(train_prog, feed=feeder.feed(data), fetch_list=[avg_loss])
            iters += 1
            num_samples += len(data)
            train_losses.append(loss)
            print(('Pass: %d, Iter: %d, Loss: %f\n' % (pass_id, iters, np.mean(train_losses))))
        print_train_time(start_time, time.time(), num_samples)
        (print(('Pass: %d, Loss: %f' % (pass_id, np.mean(train_losses)))),)
        if ((not args.no_test) and batch_acc):
            pass_test_acc = test(exe, infer_prog, test_reader, feeder, batch_acc)
            print((', Test Accuracy: %f' % pass_test_acc))
        print('\n')
        exit(0)