def _activation_summary(x):
    'Helper to create summaries for activations.\n\n  Creates a summary that provides a histogram of activations.\n  Creates a summary that measure the sparsity of activations.\n\n  Args:\n    x: Tensor\n  Returns:\n    nothing\n  '
    tensor_name = re.sub(('%s_[0-9]*/' % TOWER_NAME), '', x.op.name)
    tf.histogram_summary((tensor_name + '/activations'), x)
    tf.scalar_summary((tensor_name + '/sparsity'), tf.nn.zero_fraction(x))