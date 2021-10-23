def sequence_loss(logits, targets, weights, average_across_timesteps=True, average_across_batch=True, softmax_loss_function=None, name=None):
    'Weighted cross-entropy loss for a sequence of logits (per example).\n\n  Args:\n    logits: A 3D Tensor of shape\n      [batch_size x sequence_length x num_decoder_symbols] and dtype float.\n      The logits correspond to the prediction across all classes at each\n      timestep.\n    targets: A 2D Tensor of shape [batch_size x sequence_length] and dtype\n      int. The target represents the true class at each timestep.\n    weights: A 2D Tensor of shape [batch_size x sequence_length] and dtype\n      float. Weights constitutes the weighting of each prediction in the\n      sequence. When using weights as masking set all valid timesteps to 1 and\n      all padded timesteps to 0.\n    average_across_timesteps: If set, sum the cost across the sequence\n      dimension and divide by the cost by the total label weight across\n      timesteps.\n    average_across_batch: If set, sum the cost across the batch dimension and\n      divide the returned cost by the batch size.\n    softmax_loss_function: Function (inputs-batch, labels-batch) -> loss-batch\n      to be used instead of the standard softmax (the default if this is None).\n    name: Optional name for this operation, defaults to "sequence_loss".\n\n  Returns:\n    A scalar float Tensor: The average log-perplexity per symbol (weighted).\n\n  Raises:\n    ValueError: logits does not have 3 dimensions or targets does not have 2\n                dimensions or weights does not have 2 dimensions.\n  '
    if (len(logits.get_shape()) != 3):
        raise ValueError('Logits must be a [batch_size x sequence_length x logits] tensor')
    if (len(targets.get_shape()) != 2):
        raise ValueError('Targets must be a [batch_size x sequence_length] tensor')
    if (len(weights.get_shape()) != 2):
        raise ValueError('Weights must be a [batch_size x sequence_length] tensor')
    with ops.name_scope(name, 'sequence_loss', [logits, targets, weights]):
        num_classes = array_ops.shape(logits)[2]
        probs_flat = array_ops.reshape(logits, [(- 1), num_classes])
        targets = array_ops.reshape(targets, [(- 1)])
        if (softmax_loss_function is None):
            crossent = nn_ops.sparse_softmax_cross_entropy_with_logits(labels=targets, logits=probs_flat)
        else:
            crossent = softmax_loss_function(probs_flat, targets)
        crossent = (crossent * array_ops.reshape(weights, [(- 1)]))
        if (average_across_timesteps and average_across_batch):
            crossent = math_ops.reduce_sum(crossent)
            total_size = math_ops.reduce_sum(weights)
            total_size += 1e-12
            crossent /= total_size
        else:
            batch_size = array_ops.shape(logits)[0]
            sequence_length = array_ops.shape(logits)[1]
            crossent = array_ops.reshape(crossent, [batch_size, sequence_length])
        if (average_across_timesteps and (not average_across_batch)):
            crossent = math_ops.reduce_sum(crossent, axis=[1])
            total_size = math_ops.reduce_sum(weights, axis=[1])
            total_size += 1e-12
            crossent /= total_size
        if ((not average_across_timesteps) and average_across_batch):
            crossent = math_ops.reduce_sum(crossent, axis=[0])
            total_size = math_ops.reduce_sum(weights, axis=[0])
            total_size += 1e-12
            crossent /= total_size
        return crossent