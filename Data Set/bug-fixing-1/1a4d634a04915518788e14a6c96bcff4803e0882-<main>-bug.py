

def main(_):
    tf.logging.set_verbosity(tf.logging.INFO)
    sess = tf.InteractiveSession()
    model_settings = models.prepare_model_settings(len(input_data.prepare_words_list(FLAGS.wanted_words.split(','))), FLAGS.sample_rate, FLAGS.clip_duration_ms, FLAGS.window_size_ms, FLAGS.window_stride_ms, FLAGS.dct_coefficient_count)
    audio_processor = input_data.AudioProcessor(FLAGS.data_url, FLAGS.data_dir, FLAGS.silence_percentage, FLAGS.unknown_percentage, FLAGS.wanted_words.split(','), FLAGS.validation_percentage, FLAGS.testing_percentage, model_settings)
    fingerprint_size = model_settings['fingerprint_size']
    label_count = model_settings['label_count']
    time_shift_samples = int(((FLAGS.time_shift_ms * FLAGS.sample_rate) / 1000))
    training_steps_list = list(map(int, FLAGS.how_many_training_steps.split(',')))
    learning_rates_list = list(map(float, FLAGS.learning_rate.split(',')))
    if (len(training_steps_list) != len(learning_rates_list)):
        raise Exception(('--how_many_training_steps and --learning_rate must be equal length lists, but are %d and %d long instead' % (len(training_steps_list), len(learning_rates_list))))
    fingerprint_input = tf.placeholder(tf.float32, [None, fingerprint_size], name='fingerprint_input')
    (logits, dropout_prob) = models.create_model(fingerprint_input, model_settings, FLAGS.model_architecture, is_training=True)
    ground_truth_input = tf.placeholder(tf.float32, [None, label_count], name='groundtruth_input')
    control_dependencies = []
    if FLAGS.check_nans:
        checks = tf.add_check_numerics_ops()
        control_dependencies = [checks]
    with tf.name_scope('cross_entropy'):
        cross_entropy_mean = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=ground_truth_input, logits=logits))
    tf.summary.scalar('cross_entropy', cross_entropy_mean)
    with tf.name_scope('train'), tf.control_dependencies(control_dependencies):
        learning_rate_input = tf.placeholder(tf.float32, [], name='learning_rate_input')
        train_step = tf.train.GradientDescentOptimizer(learning_rate_input).minimize(cross_entropy_mean)
    predicted_indices = tf.argmax(logits, 1)
    expected_indices = tf.argmax(ground_truth_input, 1)
    correct_prediction = tf.equal(predicted_indices, expected_indices)
    confusion_matrix = tf.confusion_matrix(expected_indices, predicted_indices, num_classes=label_count)
    evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar('accuracy', evaluation_step)
    global_step = tf.contrib.framework.get_or_create_global_step()
    increment_global_step = tf.assign(global_step, (global_step + 1))
    saver = tf.train.Saver(tf.global_variables())
    merged_summaries = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter((FLAGS.summaries_dir + '/train'), sess.graph)
    validation_writer = tf.summary.FileWriter((FLAGS.summaries_dir + '/validation'))
    tf.global_variables_initializer().run()
    start_step = 1
    if FLAGS.start_checkpoint:
        models.load_variables_from_checkpoint(sess, FLAGS.start_checkpoint)
        start_step = global_step.eval(session=sess)
    tf.logging.info('Training from step: %d ', start_step)
    tf.train.write_graph(sess.graph_def, FLAGS.train_dir, (FLAGS.model_architecture + '.pbtxt'))
    with gfile.GFile(os.path.join(FLAGS.train_dir, (FLAGS.model_architecture + '_labels.txt')), 'w') as f:
        f.write('\n'.join(audio_processor.words_list))
    training_steps_max = np.sum(training_steps_list)
    for training_step in xrange(start_step, (training_steps_max + 1)):
        training_steps_sum = 0
        for i in range(len(training_steps_list)):
            training_steps_sum += training_steps_list[i]
            if (training_step <= training_steps_sum):
                learning_rate_value = learning_rates_list[i]
                break
        (train_fingerprints, train_ground_truth) = audio_processor.get_data(FLAGS.batch_size, 0, model_settings, FLAGS.background_frequency, FLAGS.background_volume, time_shift_samples, 'training', sess)
        (train_summary, train_accuracy, cross_entropy_value, _, _) = sess.run([merged_summaries, evaluation_step, cross_entropy_mean, train_step, increment_global_step], feed_dict={
            fingerprint_input: train_fingerprints,
            ground_truth_input: train_ground_truth,
            learning_rate_input: learning_rate_value,
            dropout_prob: 0.5,
        })
        train_writer.add_summary(train_summary, training_step)
        tf.logging.info(('Step #%d: rate %f, accuracy %.1f%%, cross entropy %f' % (training_step, learning_rate_value, (train_accuracy * 100), cross_entropy_value)))
        is_last_step = (training_step == training_steps_max)
        if (((training_step % FLAGS.eval_step_interval) == 0) or is_last_step):
            set_size = audio_processor.set_size('validation')
            total_accuracy = 0
            total_conf_matrix = None
            for i in xrange(0, set_size, FLAGS.batch_size):
                (validation_fingerprints, validation_ground_truth) = audio_processor.get_data(FLAGS.batch_size, i, model_settings, 0.0, 0.0, 0, 'validation', sess)
                (validation_summary, validation_accuracy, conf_matrix) = sess.run([merged_summaries, evaluation_step, confusion_matrix], feed_dict={
                    fingerprint_input: validation_fingerprints,
                    ground_truth_input: validation_ground_truth,
                    dropout_prob: 1.0,
                })
                validation_writer.add_summary(validation_summary, training_step)
                batch_size = min(FLAGS.batch_size, (set_size - i))
                total_accuracy += ((validation_accuracy * batch_size) / set_size)
                if (total_conf_matrix is None):
                    total_conf_matrix = conf_matrix
                else:
                    total_conf_matrix += conf_matrix
            tf.logging.info(('Confusion Matrix:\n %s' % total_conf_matrix))
            tf.logging.info(('Step %d: Validation accuracy = %.1f%% (N=%d)' % (training_step, (total_accuracy * 100), set_size)))
        if (((training_step % FLAGS.save_step_interval) == 0) or (training_step == training_steps_max)):
            checkpoint_path = os.path.join(FLAGS.train_dir, (FLAGS.model_architecture + '.ckpt'))
            tf.logging.info('Saving to "%s-%d"', checkpoint_path, training_step)
            saver.save(sess, checkpoint_path, global_step=training_step)
    set_size = audio_processor.set_size('testing')
    tf.logging.info('set_size=%d', set_size)
    total_accuracy = 0
    total_conf_matrix = None
    for i in xrange(0, set_size, FLAGS.batch_size):
        (test_fingerprints, test_ground_truth) = audio_processor.get_data(FLAGS.batch_size, i, model_settings, 0.0, 0.0, 0, 'testing', sess)
        (test_accuracy, conf_matrix) = sess.run([evaluation_step, confusion_matrix], feed_dict={
            fingerprint_input: test_fingerprints,
            ground_truth_input: test_ground_truth,
            dropout_prob: 1.0,
        })
        batch_size = min(FLAGS.batch_size, (set_size - i))
        total_accuracy += ((test_accuracy * batch_size) / set_size)
        if (total_conf_matrix is None):
            total_conf_matrix = conf_matrix
        else:
            total_conf_matrix += conf_matrix
    tf.logging.info(('Confusion Matrix:\n %s' % total_conf_matrix))
    tf.logging.info(('Final test accuracy = %.1f%% (N=%d)' % ((total_accuracy * 100), set_size)))
