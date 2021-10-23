def in_test_phase(x, alt):
    'Selects `x` in test phase, and `alt` otherwise.\n    Note that `alt` should have the *same shape* as `x`.\n    '
    if (_LEARNING_PHASE is 1):
        return alt
    elif (_LEARNING_PHASE is 0):
        return x
    x_shape = copy.copy(x.get_shape())
    x = tf.python.control_flow_ops.cond(tf.cast(_LEARNING_PHASE, 'bool'), (lambda : alt), (lambda : x))
    x._uses_learning_phase = True
    x.set_shape(x_shape)
    return x