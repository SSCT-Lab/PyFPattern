

def exponential_decay(learning_rate, global_step, decay_steps, decay_rate, staircase=False, name=None):
    "Applies exponential decay to the learning rate.\n\n  When training a model, it is often recommended to lower the learning rate as\n  the training progresses.  This function applies an exponential decay function\n  to a provided initial learning rate.  It requires a `global_step` value to\n  compute the decayed learning rate.  You can just pass a TensorFlow variable\n  that you increment at each training step.\n\n  The function returns the decayed learning rate.  It is computed as:\n\n  ```python\n  decayed_learning_rate = learning_rate *\n                          decay_rate ^ (global_step / decay_steps)\n  ```\n\n  If the argument `staircase` is `True`, then `global_step / decay_steps` is an\n  integer division and the decayed learning rate follows a staircase function.\n\n  Example: decay every 100000 steps with a base of 0.96:\n\n  ```python\n  ...\n  global_step = tf.Variable(0, trainable=False)\n  starter_learning_rate = 0.1\n  learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step,\n                                             100000, 0.96, staircase=True)\n  # Passing global_step to minimize() will increment it at each step.\n  learning_step = (\n      tf.train.GradientDescentOptimizer(learning_rate)\n      .minimize(...my loss..., global_step=global_step)\n  )\n  ```\n\n  Args:\n    learning_rate: A scalar `float32` or `float64` `Tensor` or a\n      Python number.  The initial learning rate.\n    global_step: A scalar `int32` or `int64` `Tensor` or a Python number.\n      Global step to use for the decay computation.  Must not be negative.\n    decay_steps: A scalar `int32` or `int64` `Tensor` or a Python number.\n      Must be positive.  See the decay computation above.\n    decay_rate: A scalar `float32` or `float64` `Tensor` or a\n      Python number.  The decay rate.\n    staircase: Boolean.  If `True` decay the learning rate at discrete intervals\n    name: String.  Optional name of the operation.  Defaults to\n      'ExponentialDecay'.\n\n  Returns:\n    A scalar `Tensor` of the same type as `learning_rate`.  The decayed\n    learning rate.\n\n  Raises:\n    ValueError: if `global_step` is not supplied.\n  "
    if (global_step is None):
        raise ValueError('global_step is required for exponential_decay.')
    with ops.name_scope(name, 'ExponentialDecay', [learning_rate, global_step, decay_steps, decay_rate]) as name:
        learning_rate = ops.convert_to_tensor(learning_rate, name='learning_rate')
        dtype = learning_rate.dtype
        global_step = math_ops.cast(global_step, dtype)
        decay_steps = math_ops.cast(decay_steps, dtype)
        decay_rate = math_ops.cast(decay_rate, dtype)
        p = (global_step / decay_steps)
        if staircase:
            p = math_ops.floor(p)
        return math_ops.mul(learning_rate, math_ops.pow(decay_rate, p), name=name)
