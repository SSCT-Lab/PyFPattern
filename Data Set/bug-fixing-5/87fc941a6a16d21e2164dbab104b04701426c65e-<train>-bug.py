def train(train_op, logdir, train_step_fn=train_step, train_step_kwargs=_USE_DEFAULT, log_every_n_steps=1, graph=None, master='', is_chief=True, global_step=None, number_of_steps=None, init_op=_USE_DEFAULT, init_feed_dict=None, local_init_op=_USE_DEFAULT, init_fn=None, ready_op=_USE_DEFAULT, summary_op=_USE_DEFAULT, save_summaries_secs=600, summary_writer=_USE_DEFAULT, startup_delay_steps=0, saver=None, save_interval_secs=600, sync_optimizer=None, session_config=None, session_wrapper=None, trace_every_n_steps=None, ignore_live_threads=False):
    'Runs a training loop using a TensorFlow supervisor.\n\n  When the sync_optimizer is supplied, gradient updates are applied\n  synchronously. Otherwise, gradient updates are applied asynchronous.\n\n  Args:\n    train_op: A `Tensor` that, when executed, will apply the gradients and\n      return the loss value.\n    logdir: The directory where training logs are written to. If None, model\n      checkpoints and summaries will not be written.\n    train_step_fn: The function to call in order to execute a single gradient\n      step. The function must have take exactly four arguments: the current\n      session, the `train_op` `Tensor`, a global step `Tensor` and a dictionary.\n    train_step_kwargs: A dictionary which is passed to the `train_step_fn`. By\n      default, two `Boolean`, scalar ops called "should_stop" and "should_log"\n      are provided.\n    log_every_n_steps: The frequency, in terms of global steps, that the loss\n      and global step and logged.\n    graph: The graph to pass to the supervisor. If no graph is supplied the\n      default graph is used.\n    master: The address of the tensorflow master.\n    is_chief: Specifies whether or not the training is being run by the primary\n      replica during replica training.\n    global_step: The `Tensor` representing the global step. If left as `None`,\n      then slim.variables.get_or_create_global_step() is used.\n    number_of_steps: The max number of gradient steps to take during training,\n      as measured by \'global_step\': training will stop if global_step is\n      greater than \'number_of_steps\'. If the value is left as None, training\n      proceeds indefinitely.\n    init_op: The initialization operation. If left to its default value, then\n      the session is initialized by calling `tf.global_variables_initializer()`.\n    init_feed_dict: A feed dictionary to use when executing the `init_op`.\n    local_init_op: The local initialization operation. If left to its default\n      value, then the session is initialized by calling\n      `tf.local_variables_initializer()` and `tf.tables_initializer()`.\n    init_fn: An optional callable to be executed after `init_op` is called. The\n      callable must accept one argument, the session being initialized.\n    ready_op: Operation to check if the model is ready to use. If left to its\n      default value, then the session checks for readiness by calling\n      `tf.report_uninitialized_variables()`.\n    summary_op: The summary operation.\n    save_summaries_secs: How often, in seconds, to save summaries.\n    summary_writer: `SummaryWriter` to use.  Can be `None`\n      to indicate that no summaries should be written. If unset, we\n      create a SummaryWriter.\n    startup_delay_steps: The number of steps to wait for before beginning. Note\n      that this must be 0 if a sync_optimizer is supplied.\n    saver: Saver to save checkpoints. If None, a default one will be created\n      and used.\n    save_interval_secs: How often, in seconds, to save the model to `logdir`.\n    sync_optimizer: an instance of tf.train.SyncReplicasOptimizer, or a list of\n      them. If the argument is supplied, gradient updates will be synchronous.\n      If left as `None`, gradient updates will be asynchronous.\n    session_config: An instance of `tf.ConfigProto` that will be used to\n      configure the `Session`. If left as `None`, the default will be used.\n    session_wrapper: A function that takes a `tf.Session` object as the only\n      argument and returns a wrapped session object that has the same methods\n      that the original object has, or `None`. Iff not `None`, the wrapped\n      object will be used for training.\n    trace_every_n_steps: produce and save a `Timeline` in Chrome trace format\n      and add it to the summaries every `trace_every_n_steps`. If None, no trace\n      information will be produced or saved.\n    ignore_live_threads: If `True` ignores threads that remain running after\n      a grace period when stopping the supervisor, instead of raising a\n      RuntimeError.\n\n  Returns:\n    the value of the loss function after training.\n\n  Raises:\n    ValueError: if `train_op` is empty or if `startup_delay_steps` is\n      non-zero when `sync_optimizer` is supplied, if `number_of_steps` is\n      negative, or if `trace_every_n_steps` is not `None` and no `logdir` is\n      provided.\n  '
    if (train_op is None):
        raise ValueError('train_op cannot be None.')
    if (logdir is None):
        if (summary_op != _USE_DEFAULT):
            raise ValueError('Cannot provide summary_op because logdir=None')
        if (saver is not None):
            raise ValueError('Cannot provide saver because logdir=None')
        if (trace_every_n_steps is not None):
            raise ValueError('Cannot provide trace_every_n_steps because logdir=None')
    if isinstance(sync_optimizer, sync_replicas_optimizer.SyncReplicasOptimizer):
        sync_optimizer = [sync_optimizer]
    if ((sync_optimizer is not None) and (startup_delay_steps > 0)):
        raise ValueError('startup_delay_steps must be zero when sync_optimizer is supplied.')
    if ((number_of_steps is not None) and (number_of_steps <= 0)):
        raise ValueError('`number_of_steps` must be either None or a positive number.')
    graph = (graph or ops.get_default_graph())
    with graph.as_default():
        if (global_step is None):
            global_step = training_util.get_or_create_global_step()
        saver = (saver or tf_saver.Saver())
        if (sync_optimizer is not None):
            for opt in sync_optimizer:
                if (not isinstance(opt, sync_replicas_optimizer.SyncReplicasOptimizer)):
                    raise ValueError('`sync_optimizer` must be a tf.train.SyncReplicasOptimizer.')
        with ops.name_scope('init_ops'):
            if (init_op == _USE_DEFAULT):
                init_op = variables.global_variables_initializer()
            if (ready_op == _USE_DEFAULT):
                ready_op = variables.report_uninitialized_variables()
            if (local_init_op == _USE_DEFAULT):
                local_init_op = control_flow_ops.group(variables.local_variables_initializer(), lookup_ops.tables_initializer())
            if ((sync_optimizer is not None) and isinstance(sync_optimizer, list)):
                with ops.control_dependencies(([local_init_op] if (local_init_op is not None) else [])):
                    if is_chief:
                        local_init_op = control_flow_ops.group(*[opt.chief_init_op for opt in sync_optimizer])
                    else:
                        local_init_op = control_flow_ops.group(*[opt.local_step_init_op for opt in sync_optimizer])
                ready_for_local_init_op = control_flow_ops.group(*[opt.ready_for_local_init_op for opt in sync_optimizer])
            else:
                ready_for_local_init_op = None
        if (summary_op == _USE_DEFAULT):
            summary_op = summary.merge_all()
        if (summary_writer == _USE_DEFAULT):
            summary_writer = supervisor.Supervisor.USE_DEFAULT
        if (is_chief and (sync_optimizer is not None)):
            init_tokens_op = [opt.get_init_tokens_op() for opt in sync_optimizer]
            chief_queue_runner = [opt.get_chief_queue_runner() for opt in sync_optimizer]
        if (train_step_kwargs == _USE_DEFAULT):
            with ops.name_scope('train_step'):
                train_step_kwargs = {
                    
                }
                if number_of_steps:
                    should_stop_op = math_ops.greater_equal(global_step, number_of_steps)
                else:
                    should_stop_op = constant_op.constant(False)
                train_step_kwargs['should_stop'] = should_stop_op
                if (log_every_n_steps > 0):
                    train_step_kwargs['should_log'] = math_ops.equal(math_ops.mod(global_step, log_every_n_steps), 0)
                if (is_chief and (trace_every_n_steps is not None)):
                    train_step_kwargs['should_trace'] = math_ops.equal(math_ops.mod(global_step, trace_every_n_steps), 0)
                    train_step_kwargs['logdir'] = logdir
    sv = supervisor.Supervisor(graph=graph, is_chief=is_chief, logdir=logdir, init_op=init_op, init_feed_dict=init_feed_dict, local_init_op=local_init_op, ready_for_local_init_op=ready_for_local_init_op, ready_op=ready_op, summary_op=summary_op, summary_writer=summary_writer, global_step=global_step, saver=saver, save_summaries_secs=save_summaries_secs, save_model_secs=save_interval_secs, init_fn=init_fn)
    if (summary_writer is not None):
        train_step_kwargs['summary_writer'] = sv.summary_writer
    total_loss = None
    should_retry = True
    while should_retry:
        try:
            should_retry = False
            with sv.managed_session(master, start_standard_services=False, config=session_config) as sess:
                logging.info('Starting Session.')
                if (session_wrapper is not None):
                    logging.info('Wrapping session with wrapper function: %s', session_wrapper)
                    sess = session_wrapper(sess)
                if is_chief:
                    if logdir:
                        sv.start_standard_services(sess)
                elif (startup_delay_steps > 0):
                    _wait_for_step(sess, global_step, min(startup_delay_steps, (number_of_steps or sys.maxsize)))
                threads = sv.start_queue_runners(sess)
                logging.info('Starting Queues.')
                if (is_chief and (sync_optimizer is not None)):
                    sv.start_queue_runners(sess, chief_queue_runner)
                    sess.run(init_tokens_op)
                try:
                    while (not sv.should_stop()):
                        (total_loss, should_stop) = train_step_fn(sess, train_op, global_step, train_step_kwargs)
                        if should_stop:
                            logging.info('Stopping Training.')
                            sv.request_stop()
                            break
                except errors.OutOfRangeError as e:
                    logging.info('Caught OutOfRangeError. Stopping Training. %s', e)
                if (logdir and sv.is_chief):
                    logging.info('Finished training! Saving model to disk.')
                    sv.saver.save(sess, sv.save_path, global_step=sv.global_step)
                    sv.stop(threads, close_summary_writer=True, ignore_live_threads=ignore_live_threads)
        except errors.AbortedError:
            logging.info('Retrying training!')
            should_retry = True
    return total_loss