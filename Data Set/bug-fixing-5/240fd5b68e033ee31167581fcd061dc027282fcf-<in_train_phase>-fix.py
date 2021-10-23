def in_train_phase(x, alt):
    'Selects `x` in train phase, and `alt` otherwise.\n    Note that `alt` should have the *same shape* as `x`.\n    '
    if (_LEARNING_PHASE is 1):
        return x
    elif (_LEARNING_PHASE is 0):
        return alt
    x_shape = copy.copy(x.get_shape())
    x = control_flow_ops.cond(tf.cast(_LEARNING_PHASE, 'bool'), (lambda : x), (lambda : alt))
    x._uses_learning_phase = True
    x.set_shape(x_shape)
    return x