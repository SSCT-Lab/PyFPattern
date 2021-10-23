def decode():
    with tf.Session() as sess:
        model = create_model(sess, True)
        model.batch_size = 1
        en_vocab_path = os.path.join(FLAGS.data_dir, ('vocab%d.en' % FLAGS.en_vocab_size))
        fr_vocab_path = os.path.join(FLAGS.data_dir, ('vocab%d.fr' % FLAGS.fr_vocab_size))
        (en_vocab, _) = data_utils.initialize_vocabulary(en_vocab_path)
        (_, rev_fr_vocab) = data_utils.initialize_vocabulary(fr_vocab_path)
        sys.stdout.write('> ')
        sys.stdout.flush()
        sentence = sys.stdin.readline()
        while sentence:
            token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), en_vocab)
            bucket_id = (len(_buckets) - 1)
            for (i, bucket) in enumerate(_buckets):
                if (bucket[0] >= len(token_ids)):
                    bucket_id = i
                    break
            else:
                logging.warning('Sentence truncated: %s', sentence)
            (encoder_inputs, decoder_inputs, target_weights) = model.get_batch({
                bucket_id: [(token_ids, [])],
            }, bucket_id)
            (_, _, output_logits) = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)
            outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
            if (data_utils.EOS_ID in outputs):
                outputs = outputs[:outputs.index(data_utils.EOS_ID)]
            print(' '.join([tf.compat.as_str(rev_fr_vocab[output]) for output in outputs]))
            print('> ', end='')
            sys.stdout.flush()
            sentence = sys.stdin.readline()