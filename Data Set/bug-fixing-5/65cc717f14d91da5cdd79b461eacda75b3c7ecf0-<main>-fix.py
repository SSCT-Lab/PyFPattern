def main(unused_argv):
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)
    if FLAGS.download_only:
        sys.exit(0)
    if ((FLAGS.job_name is None) or (FLAGS.job_name == '')):
        raise ValueError('Must specify an explicit `job_name`')
    if ((FLAGS.task_index is None) or (FLAGS.task_index == '')):
        raise ValueError('Must specify an explicit `task_index`')
    print(('job name = %s' % FLAGS.job_name))
    print(('task index = %d' % FLAGS.task_index))
    ps_spec = FLAGS.ps_hosts.split(',')
    worker_spec = FLAGS.worker_hosts.split(',')
    num_workers = len(worker_spec)
    cluster = tf.train.ClusterSpec({
        'ps': ps_spec,
        'worker': worker_spec,
    })
    if (not FLAGS.existing_servers):
        server = tf.train.Server(cluster, job_name=FLAGS.job_name, task_index=FLAGS.task_index)
        if (FLAGS.job_name == 'ps'):
            server.join()
    is_chief = (FLAGS.task_index == 0)
    if (FLAGS.num_gpus > 0):
        gpu = (FLAGS.task_index % FLAGS.num_gpus)
        worker_device = ('/job:worker/task:%d/gpu:%d' % (FLAGS.task_index, gpu))
    elif (FLAGS.num_gpus == 0):
        cpu = 0
        worker_device = ('/job:worker/task:%d/cpu:%d' % (FLAGS.task_index, cpu))
    with tf.device(tf.train.replica_device_setter(worker_device=worker_device, ps_device='/job:ps/cpu:0', cluster=cluster)):
        global_step = tf.Variable(0, name='global_step', trainable=False)
        hid_w = tf.Variable(tf.truncated_normal([(IMAGE_PIXELS * IMAGE_PIXELS), FLAGS.hidden_units], stddev=(1.0 / IMAGE_PIXELS)), name='hid_w')
        hid_b = tf.Variable(tf.zeros([FLAGS.hidden_units]), name='hid_b')
        sm_w = tf.Variable(tf.truncated_normal([FLAGS.hidden_units, 10], stddev=(1.0 / math.sqrt(FLAGS.hidden_units))), name='sm_w')
        sm_b = tf.Variable(tf.zeros([10]), name='sm_b')
        x = tf.placeholder(tf.float32, [None, (IMAGE_PIXELS * IMAGE_PIXELS)])
        y_ = tf.placeholder(tf.float32, [None, 10])
        hid_lin = tf.nn.xw_plus_b(x, hid_w, hid_b)
        hid = tf.nn.relu(hid_lin)
        y = tf.nn.softmax(tf.nn.xw_plus_b(hid, sm_w, sm_b))
        cross_entropy = (- tf.reduce_sum((y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))))
        opt = tf.train.AdamOptimizer(FLAGS.learning_rate)
        if FLAGS.sync_replicas:
            if (FLAGS.replicas_to_aggregate is None):
                replicas_to_aggregate = num_workers
            else:
                replicas_to_aggregate = FLAGS.replicas_to_aggregate
            opt = tf.train.SyncReplicasOptimizer(opt, replicas_to_aggregate=replicas_to_aggregate, total_num_replicas=num_workers, name='mnist_sync_replicas')
        train_step = opt.minimize(cross_entropy, global_step=global_step)
        if FLAGS.sync_replicas:
            local_init_op = opt.local_step_init_op
            if is_chief:
                local_init_op = opt.chief_init_op
            ready_for_local_init_op = opt.ready_for_local_init_op
            chief_queue_runner = opt.get_chief_queue_runner()
            sync_init_op = opt.get_init_tokens_op()
        init_op = tf.global_variables_initializer()
        train_dir = tempfile.mkdtemp()
        if FLAGS.sync_replicas:
            sv = tf.train.Supervisor(is_chief=is_chief, logdir=train_dir, init_op=init_op, local_init_op=local_init_op, ready_for_local_init_op=ready_for_local_init_op, recovery_wait_secs=1, global_step=global_step)
        else:
            sv = tf.train.Supervisor(is_chief=is_chief, logdir=train_dir, init_op=init_op, recovery_wait_secs=1, global_step=global_step)
        sess_config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False, device_filters=['/job:ps', ('/job:worker/task:%d' % FLAGS.task_index)])
        if is_chief:
            print(('Worker %d: Initializing session...' % FLAGS.task_index))
        else:
            print(('Worker %d: Waiting for session to be initialized...' % FLAGS.task_index))
        if FLAGS.existing_servers:
            server_grpc_url = ('grpc://' + worker_spec[FLAGS.task_index])
            print(('Using existing server at: %s' % server_grpc_url))
            sess = sv.prepare_or_wait_for_session(server_grpc_url, config=sess_config)
        else:
            sess = sv.prepare_or_wait_for_session(server.target, config=sess_config)
        print(('Worker %d: Session initialization complete.' % FLAGS.task_index))
        if (FLAGS.sync_replicas and is_chief):
            sess.run(sync_init_op)
            sv.start_queue_runners(sess, [chief_queue_runner])
        time_begin = time.time()
        print(('Training begins @ %f' % time_begin))
        local_step = 0
        while True:
            (batch_xs, batch_ys) = mnist.train.next_batch(FLAGS.batch_size)
            train_feed = {
                x: batch_xs,
                y_: batch_ys,
            }
            (_, step) = sess.run([train_step, global_step], feed_dict=train_feed)
            local_step += 1
            now = time.time()
            print(('%f: Worker %d: training step %d done (global step: %d)' % (now, FLAGS.task_index, local_step, step)))
            if (step >= FLAGS.train_steps):
                break
        time_end = time.time()
        print(('Training ends @ %f' % time_end))
        training_time = (time_end - time_begin)
        print(('Training elapsed time: %f s' % training_time))
        val_feed = {
            x: mnist.validation.images,
            y_: mnist.validation.labels,
        }
        val_xent = sess.run(cross_entropy, feed_dict=val_feed)
        print(('After %d training step(s), validation cross entropy = %g' % (FLAGS.train_steps, val_xent)))