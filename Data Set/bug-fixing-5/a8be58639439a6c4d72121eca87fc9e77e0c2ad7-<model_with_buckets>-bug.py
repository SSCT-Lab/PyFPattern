def model_with_buckets(encoder_inputs, decoder_inputs, targets, weights, buckets, seq2seq, softmax_loss_function=None, per_example_loss=False, name=None):
    'Create a sequence-to-sequence model with support for bucketing.\n\n  The seq2seq argument is a function that defines a sequence-to-sequence model,\n  e.g., seq2seq = lambda x, y: basic_rnn_seq2seq(x, y, rnn_cell.GRUCell(24))\n\n  Args:\n    encoder_inputs: A list of Tensors to feed the encoder; first seq2seq input.\n    decoder_inputs: A list of Tensors to feed the decoder; second seq2seq input.\n    targets: A list of 1D batch-sized int32 Tensors (desired output sequence).\n    weights: List of 1D batch-sized float-Tensors to weight the targets.\n    buckets: A list of pairs of (input size, output size) for each bucket.\n    seq2seq: A sequence-to-sequence model function; it takes 2 input that\n      agree with encoder_inputs and decoder_inputs, and returns a pair\n      consisting of outputs and states (as, e.g., basic_rnn_seq2seq).\n    softmax_loss_function: Function (inputs-batch, labels-batch) -> loss-batch\n      to be used instead of the standard softmax (the default if this is None).\n    per_example_loss: Boolean. If set, the returned loss will be a batch-sized\n      tensor of losses for each sequence in the batch. If unset, it will be\n      a scalar with the averaged loss from all examples.\n    name: Optional name for this operation, defaults to "model_with_buckets".\n\n  Returns:\n    A tuple of the form (outputs, losses), where:\n      outputs: The outputs for each bucket. Its j\'th element consists of a list\n        of 2D Tensors of shape [batch_size x num_decoder_symbols] (jth outputs).\n      losses: List of scalar Tensors, representing losses for each bucket, or,\n        if per_example_loss is set, a list of 1D batch-sized float Tensors.\n\n  Raises:\n    ValueError: If length of encoder_inputsut, targets, or weights is smaller\n      than the largest (last) bucket.\n  '
    if (len(encoder_inputs) < buckets[(- 1)][0]):
        raise ValueError(('Length of encoder_inputs (%d) must be at least that of last bucket (%d).' % (len(encoder_inputs), buckets[(- 1)][0])))
    if (len(targets) < buckets[(- 1)][1]):
        raise ValueError(('Length of targets (%d) must be at least that of lastbucket (%d).' % (len(targets), buckets[(- 1)][1])))
    if (len(weights) < buckets[(- 1)][1]):
        raise ValueError(('Length of weights (%d) must be at least that of lastbucket (%d).' % (len(weights), buckets[(- 1)][1])))
    all_inputs = (((encoder_inputs + decoder_inputs) + targets) + weights)
    losses = []
    outputs = []
    with ops.name_scope(name, 'model_with_buckets', all_inputs):
        for (j, bucket) in enumerate(buckets):
            with variable_scope.variable_scope(variable_scope.get_variable_scope(), reuse=(True if (j > 0) else None)):
                (bucket_outputs, _) = seq2seq(encoder_inputs[:bucket[0]], decoder_inputs[:bucket[1]])
                outputs.append(bucket_outputs)
                if per_example_loss:
                    losses.append(sequence_loss_by_example(outputs[(- 1)], targets[:bucket[1]], weights[:bucket[1]], softmax_loss_function=softmax_loss_function))
                else:
                    losses.append(sequence_loss(outputs[(- 1)], targets[:bucket[1]], weights[:bucket[1]], softmax_loss_function=softmax_loss_function))
    return (outputs, losses)