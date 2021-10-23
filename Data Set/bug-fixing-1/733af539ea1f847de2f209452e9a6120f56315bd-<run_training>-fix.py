

def run_training():
    'Train MNIST for a number of epochs.'
    data_sets = input_data.read_data_sets(FLAGS.train_dir, FLAGS.fake_data)
    with tf.Graph().as_default():
        with tf.name_scope('input'):
            images_initializer = tf.placeholder(dtype=data_sets.train.images.dtype, shape=data_sets.train.images.shape)
            labels_initializer = tf.placeholder(dtype=data_sets.train.labels.dtype, shape=data_sets.train.labels.shape)
            input_images = tf.Variable(images_initializer, trainable=False, collections=[])
            input_labels = tf.Variable(labels_initializer, trainable=False, collections=[])
            (image, label) = tf.train.slice_input_producer([input_images, input_labels], num_epochs=FLAGS.num_epochs)
            label = tf.cast(label, tf.int32)
            (images, labels) = tf.train.batch([image, label], batch_size=FLAGS.batch_size)
        logits = mnist.inference(images, FLAGS.hidden1, FLAGS.hidden2)
        loss = mnist.loss(logits, labels)
        train_op = mnist.training(loss, FLAGS.learning_rate)
        eval_correct = mnist.evaluation(logits, labels)
        summary_op = tf.summary.merge_all()
        saver = tf.train.Saver()
        init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        sess = tf.Session()
        sess.run(init_op)
        sess.run(input_images.initializer, feed_dict={
            images_initializer: data_sets.train.images,
        })
        sess.run(input_labels.initializer, feed_dict={
            labels_initializer: data_sets.train.labels,
        })
        summary_writer = tf.summary.FileWriter(FLAGS.train_dir, sess.graph)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        try:
            step = 0
            while (not coord.should_stop()):
                start_time = time.time()
                (_, loss_value) = sess.run([train_op, loss])
                duration = (time.time() - start_time)
                if ((step % 100) == 0):
                    print(('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration)))
                    summary_str = sess.run(summary_op)
                    summary_writer.add_summary(summary_str, step)
                    step += 1
                if (((step + 1) % 1000) == 0):
                    print('Saving')
                    saver.save(sess, FLAGS.train_dir, global_step=step)
                step += 1
        except tf.errors.OutOfRangeError:
            print('Saving')
            saver.save(sess, FLAGS.train_dir, global_step=step)
            print(('Done training for %d epochs, %d steps.' % (FLAGS.num_epochs, step)))
        finally:
            coord.request_stop()
        coord.join(threads)
        sess.close()
