

def _GetBatchNormParams(graph, context, has_scaling):
    'Extracts relevant tensors for folding batch norms.\n\n  Args:\n    graph: Graph to inspect.\n    context: The scope under which we look for batch norm params\n    has_scaling: Bool that specifies if scaling is done as part of batch norm.\n\n  Returns:\n    _BatchNormMatch containing all required batch norm parameters.\n  '
    gamma_tensor = None
    batch_mean_tensor = None
    batch_variance_tensor = None
    moving_mean_tensor = None
    moving_variance_tensor = None
    batch_epsilon = None
    bn_decay_mean_tensor = None
    bn_decay_var_tensor = None
    split_context = context.split('/')
    base_context = split_context[(- 1)]
    oplist = graph.get_operations()
    op_suffix_mean = (base_context + '/BatchNorm/moments/Squeeze')
    op_suffix_variance = (base_context + '/BatchNorm/moments/Squeeze_1')
    op_suffix_epsilon = (base_context + '/BatchNorm/batchnorm/add/y')
    op_suffix_bn_decay_mean = (base_context + '/BatchNorm/AssignMovingAvg/decay')
    op_suffix_bn_decay_var = (base_context + '/BatchNorm/AssignMovingAvg_1/decay')
    if variable_scope.get_variable_scope().use_resource:
        op_suffix_gamma = (base_context + '/BatchNorm/gamma/Read/ReadVariableOp')
        op_suffix_moving_variance = (base_context + '/BatchNorm/moving_variance/Read/ReadVariableOp')
        op_suffix_moving_mean = (base_context + '/BatchNorm/moving_mean/Read/ReadVariableOp')
    else:
        op_suffix_gamma = (base_context + '/BatchNorm/gamma')
        op_suffix_moving_variance = (base_context + '/BatchNorm/moving_variance/read')
        op_suffix_moving_mean = (base_context + '/BatchNorm/moving_mean/read')
    for op in oplist:
        if op.name.endswith(op_suffix_mean):
            batch_mean_tensor = graph.get_tensor_by_name((op.name + ':0'))
        if op.name.endswith(op_suffix_variance):
            batch_variance_tensor = graph.get_tensor_by_name((op.name + ':0'))
        if op.name.endswith(op_suffix_moving_mean):
            moving_mean_tensor = graph.get_tensor_by_name((op.name + ':0'))
        if op.name.endswith(op_suffix_moving_variance):
            moving_variance_tensor = graph.get_tensor_by_name((op.name + ':0'))
        if op.name.endswith(op_suffix_epsilon):
            batch_epsilon = graph.get_tensor_by_name((op.name + ':0'))
        if op.name.endswith(op_suffix_bn_decay_mean):
            bn_decay_mean_tensor = graph.get_tensor_by_name((op.name + ':0'))
        if op.name.endswith(op_suffix_bn_decay_var):
            bn_decay_var_tensor = graph.get_tensor_by_name((op.name + ':0'))
        if has_scaling:
            if op.name.endswith(op_suffix_gamma):
                gamma_tensor = graph.get_tensor_by_name((op.name + ':0'))
    if (not has_scaling):
        gamma_tensor = array_ops.ones(moving_mean_tensor.shape)
    return _BatchNormMatch(layer_op=None, bn_op=None, output_tensor=None, input_tensor=None, weight_tensor=None, gamma_tensor=gamma_tensor, beta_tensor=None, mean_tensor=batch_mean_tensor, variance_tensor=batch_variance_tensor, moving_mean_tensor=moving_mean_tensor, moving_variance_tensor=moving_variance_tensor, bn_decay_mean_tensor=bn_decay_mean_tensor, bn_decay_var_tensor=bn_decay_var_tensor, batch_epsilon=batch_epsilon)
