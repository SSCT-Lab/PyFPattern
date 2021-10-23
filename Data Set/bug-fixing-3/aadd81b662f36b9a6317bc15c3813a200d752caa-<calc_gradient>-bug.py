def calc_gradient(targets, inputs, target_gradients=None, no_grad_set=None):
    '\n    Backpropagate the gradients of targets to inputs.\n\n    Args:\n        targets(Variable|list[Variable]): The target variables\n        inputs(Variable|list[Variable]): The input variables\n        target_gradients (Variable|list[Variable]|None): The gradient variables\n            of targets which has the same shape with targets, If None, ones will\n            be created for them.\n        no_grad_set(set[string]): The names of variables that have no gradients\n            in Block 0. All variables with `stop_gradient=True` from all blocks\n            will be automatically added.\n\n    Return:\n        (list[Variable]): A list of gradients for inputs\n        If an input does not affect targets, the corresponding gradient variable\n        will be None\n    '
    targets = _as_list(targets)
    inputs = _as_list(inputs)
    target_gradients = _as_list(target_gradients)
    block = targets[0].block
    prog = block.program
    prog._appending_grad_times += 1
    block_idx = block.idx
    if (not target_gradients):
        target_gradients = ([None] * len(targets))
    if (len(targets) != len(target_gradients)):
        raise ValueError('Should have the same number of target_gradients as targets')
    if (no_grad_set is None):
        no_grad_set = set()
    no_grad_set = copy.copy(no_grad_set)
    no_grad_dict = _get_stop_gradients_(prog)
    no_grad_dict[0].update(list(map(_append_grad_suffix_, no_grad_set)))
    fwd_op_num = block.desc.op_size()
    input_grad_names_set = set()
    target_grad_map = {
        
    }
    for (i, grad) in enumerate(target_gradients):
        target = targets[i]
        if (grad is None):
            grad_name = _append_grad_suffix_(target.name)
            target_shape = paddle.fluid.layers.shape(target)
            op_desc = _create_op_desc_('fill_constant', {
                'ShapeTensor': [target_shape.name],
            }, {
                'Out': [grad_name],
            }, {
                'shape': target.shape,
                'value': 1.0,
                'dtype': target.dtype,
            })
            block.desc.append_op().copy_from(op_desc)
            input_grad_names_set.add(grad_name)
        else:
            if ((target.block.idx != block_idx) or (target.block.program != prog)):
                raise ValueError('all targets must be in the same block')
            if (target.shape != grad.shape):
                raise ValueError(('The shapes of target and grad are different: %s %s' % (target.name, grad.name)))
            target_grad_map[_append_grad_suffix_(target.name)] = grad.name
            input_grad_names_set.add(grad.name)
    if (prog._appending_grad_times == 1):
        input_grad_names_set = None
    for input in inputs:
        if (input.block.program != prog):
            raise 'input must be in the same program as targets'
    block_no_grad_set = set(map(_strip_grad_suffix_, no_grad_dict[0]))
    op_path = _find_op_path_(block, targets, inputs, block_no_grad_set)
    no_grad_dict[0].update(list(map(_append_grad_suffix_, block_no_grad_set)))
    grad_to_var = dict()
    grad_info_map = dict()
    _append_backward_ops_(block, op_path, block, no_grad_dict, grad_to_var, input_grad_names_set=input_grad_names_set)
    _rename_grad_(block, fwd_op_num, grad_to_var, target_grad_map)
    _append_backward_vars_(block, fwd_op_num, grad_to_var, grad_info_map)
    prog._sync_with_cpp()
    grad_vars = []
    for input_var in inputs:
        if (input_var.name not in grad_info_map):
            grad_vars.append(None)
        else:
            grad_info = grad_info_map[input_var.name]
            grad_block = grad_info[1]
            grad_var = grad_block.var(grad_info[0])
            grad_vars.append(grad_var)
    if (len(grad_vars) == 1):
        return grad_vars[0]
    else:
        return grad_vars