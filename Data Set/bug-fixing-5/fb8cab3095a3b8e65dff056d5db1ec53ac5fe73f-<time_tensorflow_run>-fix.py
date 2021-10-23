def time_tensorflow_run(session, target, info_string):
    "Run the computation to obtain the target tensor and print timing stats.\n\n  Args:\n    session: the TensorFlow session to run the computation under.\n    target: the target Tensor that is passed to the session's run() function.\n    info_string: a string summarizing this run, to be printed with the stats.\n\n  Returns:\n    None\n  "
    num_steps_burn_in = 10
    total_duration = 0.0
    total_duration_squared = 0.0
    for i in xrange((FLAGS.num_batches + num_steps_burn_in)):
        start_time = time.time()
        _ = session.run(target)
        duration = (time.time() - start_time)
        if (i >= num_steps_burn_in):
            if (not (i % 10)):
                print(('%s: step %d, duration = %.3f' % (datetime.now(), (i - num_steps_burn_in), duration)))
            total_duration += duration
            total_duration_squared += (duration * duration)
    mn = (total_duration / FLAGS.num_batches)
    vr = ((total_duration_squared / FLAGS.num_batches) - (mn * mn))
    sd = math.sqrt(vr)
    print(('%s: %s across %d steps, %.3f +/- %.3f sec / batch' % (datetime.now(), info_string, FLAGS.num_batches, mn, sd)))