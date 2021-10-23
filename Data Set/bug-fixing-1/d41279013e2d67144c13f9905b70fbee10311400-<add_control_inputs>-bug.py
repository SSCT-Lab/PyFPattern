

def add_control_inputs(op, cops):
    'Add the control inputs cops to co.\n\n  Warning: this function is directly manipulating the internals of the tf.Graph.\n\n  Args:\n    op: a tf.Operation to which the control inputs are added.\n    cops: an object convertible to a list of `tf.Operation`.\n  Raises:\n    TypeError: if op is not a tf.Operation\n    ValueError: if any cop in cops is already a control input of op.\n  '
    if (not isinstance(op, tf_ops.Operation)):
        raise TypeError('Expected a tf.Operation, got: {}', type(op))
    cops = util.make_list_of_op(cops, allow_graph=False)
    for cop in cops:
        if (cop in op.control_inputs):
            raise ValueError('{} is already a control_input of {}'.format(op.name, cop.name))
    op._control_inputs += cops
    op._recompute_node_def()
