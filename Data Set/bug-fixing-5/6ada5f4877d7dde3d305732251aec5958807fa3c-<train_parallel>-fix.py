def train_parallel(avg_loss, infer_prog, optimizer, train_reader, test_reader, batch_acc, args, train_prog, startup_prog, nccl_id_var, num_trainers, trainer_id):
    feed_var_list = [var for var in train_prog.global_block().vars.itervalues() if var.is_data]
    if args.use_fake_data:
        for var in feed_var_list:
            v = startup_prog.global_block().clone_variable(var)
            var.persistable = True
            v.persistable = True
            real_shape = list(var.shape)
            real_shape[0] = (args.batch_size / args.gpus)
            startup_prog.global_block().append_op(outputs={
                'Out': v,
            }, type='fill_constant', attrs={
                'shape': real_shape,
                'value': 1.0,
                'dtype': var.dtype,
            })
    place = (core.CPUPlace() if (args.device == 'CPU') else core.CUDAPlace(0))
    if (nccl_id_var and (trainer_id == 0)):
        time.sleep(30)
    startup_exe = fluid.Executor(place)
    startup_exe.run(startup_prog)
    strategy = fluid.ExecutionStrategy()
    strategy.num_threads = 1
    strategy.allow_op_delay = False
    exe = fluid.ParallelExecutor(True, avg_loss.name, exec_strategy=strategy, num_trainers=num_trainers, trainer_id=trainer_id)
    feeder = fluid.DataFeeder(feed_var_list, place)
    for pass_id in range(args.pass_num):
        num_samples = 0
        iters = 0
        start_time = time.time()
        for (batch_id, data) in enumerate(train_reader()):
            if (args.profile and (pass_id == 0) and (batch_id == 5)):
                profiler.start_profiler('All')
            elif (args.profile and (pass_id == 0) and (batch_id == 10)):
                profiler.stop_profiler('total', ('/tmp/profile_%d' % trainer_id))
            if (iters == args.skip_batch_num):
                start_time = time.time()
                num_samples = 0
            if (iters == args.iterations):
                break
            if args.use_fake_data:
                (loss,) = exe.run([avg_loss.name])
            else:
                (loss,) = exe.run([avg_loss.name], feed=feeder.feed(data))
            if (args.update_method == 'pserver'):
                exe.bcast_params()
            num_samples += len(data)
            iters += 1
            if ((batch_id % 1) == 0):
                print(('Pass %d, batch %d, loss %s' % (pass_id, batch_id, np.array(loss))))
        print_train_time(start_time, time.time(), num_samples)
        if ((not args.no_test) and batch_acc):
            test_acc = test(startup_exe, infer_prog, test_reader, feeder, batch_acc)
            print(('Pass: %d, Test Accuracy: %f\n' % (pass_id, test_acc)))
        exit(0)