def sequence_loss(logits, targets, weights, average_across_timesteps=True, average_across_batch=True, softmax_loss_function=None, name=None):
    'Weighted cross-entropy loss for a sequence of logits, batch-collapsed.\n\n  Args:\n    logits: List of 2D Tensors of shape [batch_size x num_decoder_symbols].\n    targets: List of 1D batch-sized int32 Tensors of the same length as logits.\n    weights: List of 1D batch-sized float-Tensors of the same length as logits.\n    average_across_timesteps: If set, divide the returned cost by the total\n      label weight.\n    average_across_batch: If set, divide the returned cost by the batch size.\n    softmax_loss_function: Function (labels-batch, inputs-batch) -> loss-batch\n      to be used instead of the standard softmax (the default if this is None).\n    name: Optional name for this operation, defaults to "sequence_loss".\n\n  Returns:\n    A scalar float Tensor: The average log-perplexity per symbol (weighted).\n\n  Raises:\n    ValueError: If len(logits) is different from len(targets) or len(weights).\n  '
    with ops.name_scope(name, 'sequence_loss', ((logits + targets) + weights)):
        cost = math_ops.reduce_sum(sequence_loss_by_example(logits, targets, weights, average_across_timesteps=average_across_timesteps, softmax_loss_function=softmax_loss_function))
        if average_across_batch:
            batch_size = array_ops.shape(targets[0])[0]
            return (cost / math_ops.cast(batch_size, cost.dtype))
        else:
            return cost