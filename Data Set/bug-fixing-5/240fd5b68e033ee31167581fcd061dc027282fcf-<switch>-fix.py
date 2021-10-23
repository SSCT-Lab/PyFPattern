def switch(condition, then_expression, else_expression):
    'Switches between two operations depending on a scalar value (int or bool).\n    Note that both `then_expression` and `else_expression`\n    should be symbolic tensors of the *same shape*.\n\n    # Arguments\n        condition: scalar tensor.\n        then_expression: TensorFlow operation.\n        else_expression: TensorFlow operation.\n    '
    x_shape = copy.copy(then_expression.get_shape())
    x = control_flow_ops.cond(tf.cast(condition, 'bool'), (lambda : then_expression), (lambda : else_expression))
    x.set_shape(x_shape)
    return x