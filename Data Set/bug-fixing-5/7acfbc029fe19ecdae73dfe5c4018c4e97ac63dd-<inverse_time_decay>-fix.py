def inverse_time_decay(learning_rate, global_step, decay_steps, decay_rate, staircase=False, name=None):
    "Applies inverse time decay to the initial learning rate.\n\n  When training a model, it is often recommended to lower the learning rate as\n  the training progresses.  This function applies an inverse decay function\n  to a provided initial learning rate.  It requires an `global_step` value to\n  compute the decayed learning rate.  You can just pass a TensorFlow variable\n  that you increment at each training step.\n\n  The function returns the decayed learning rate.  It is computed as:\n\n  ```python\n  decayed_learning_rate = learning_rate / (1 + decay_rate * global_step / decay_step)\n  ```\n\n  or, if `staircase` is `True`, as:\n\n  ```python\n  decayed_learning_rate = learning_rate / (1 + decay_rate * floor(global_step / decay_step))\n  ```\n\n  Example: decay 1/t with a rate of 0.5:\n\n  ```python\n  ...\n  global_step = tf.Variable(0, trainable=False)\n  learning_rate = 0.1\n  decay_steps = 1.0\n  decay_rate = 0.5\n  learning_rate = tf.train.inverse_time_decay(learning_rate, global_step, decay_steps, decay_rate)\n\n  # Passing global_step to minimize() will increment it at each step.\n  learning_step = (\n      tf.train.GradientDescentOptimizer(learning_rate)\n      .minimize(...my loss..., global_step=global_step)\n  )\n  ```\n\n  Args:\n    learning_rate: A scalar `float32` or `float64` `Tensor` or a\n      Python number.  The initial learning rate.\n    global_step: A Python number.\n      Global step to use for the decay computation.  Must not be negative.\n    decay_steps: How often to apply decay.\n    decay_rate: A Python number.  The decay rate.\n    staircase: Whether to apply decay in a discrete staircase, as opposed to\n      continuous, fashion.\n    name: String.  Optional name of the operation.  Defaults to\n      'InverseTimeDecay'.\n\n  Returns:\n    A scalar `Tensor` of the same type as `learning_rate`.  The decayed\n    learning rate.\n\n  Raises:\n    ValueError: if `global_step` is not supplied.\n  "
    if (global_step is None):
        raise ValueError('global_step is required for inverse_time_decay.')
    with ops.name_scope(name, 'InverseTimeDecay', [learning_rate, global_step, decay_rate]) as name:
        learning_rate = ops.convert_to_tensor(learning_rate, name='learning_rate')
        dtype = learning_rate.dtype
        global_step = math_ops.cast(global_step, dtype)
        decay_steps = math_ops.cast(decay_steps, dtype)
        decay_rate = math_ops.cast(decay_rate, dtype)
        p = (global_step / decay_steps)
        if staircase:
            p = math_ops.floor(p)
        const = math_ops.cast(constant_op.constant(1), learning_rate.dtype)
        denom = math_ops.add(const, math_ops.multiply(decay_rate, p))
        return math_ops.div(learning_rate, denom, name=name)