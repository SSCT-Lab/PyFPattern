def ctc_decode(y_pred, input_length, greedy=True, beam_width=100, top_paths=1):
    'Decodes the output of a softmax using either\n       greedy (also known as best path) or a constrained dictionary\n       search.\n\n    # Arguments\n        y_pred: tensor `(samples, time_steps, num_categories)` containing the prediction,\n                or output of the softmax.\n        input_length: tensor `(samples, )` containing the sequence length for\n                each batch item in `y_pred`.\n        greedy: perform much faster best-path search if `true`. This does\n                not use a dictionary\n        beam_width: if `greedy` is `false`: a beam search decoder will be used\n                with a beam of this width\n        top_paths: if `greedy` is `false`: how many of the most probable paths will be returned\n\n    # Returns\n        Tuple:\n            List: if `greedy` is `true`, returns a list of one element that contains\n                the decoded sequence. If `false`, returns the `top_paths` most probable\n                decoded sequences. Important: blank labels are returned as `-1`.\n            Tensor `(top_paths, )` that contains the log probability of each decoded sequence\n    '
    y_pred = tf.log((tf.transpose(y_pred, perm=[1, 0, 2]) + 1e-08))
    input_length = tf.to_int32(input_length)
    if greedy:
        (decoded, log_prob) = ctc.ctc_greedy_decoder(inputs=y_pred, sequence_length=input_length)
    else:
        (decoded, log_prob) = ctc.ctc_beam_search_decoder(inputs=y_pred, sequence_length=input_length, beam_width=beam_width, top_paths=top_paths)
    if (tf_major_version >= 1):
        decoded_dense = [tf.sparse_to_dense(st.indices, st.dense_shape, st.values, default_value=(- 1)) for st in decoded]
    else:
        decoded_dense = [tf.sparse_to_dense(st.indices, st.shape, st.values, default_value=(- 1)) for st in decoded]
    return (decoded_dense, log_prob)