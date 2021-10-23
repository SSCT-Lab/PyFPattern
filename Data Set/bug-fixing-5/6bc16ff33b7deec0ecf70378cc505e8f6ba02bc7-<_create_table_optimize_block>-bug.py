def _create_table_optimize_block(self, pserver_index, pserver_program, pre_block_idx, grad_to_block_id):
    origin_param_var = self.origin_program.global_block().vars[self.table_name]
    zero_dim = int(math.ceil((origin_param_var.shape[0] / len(self.pserver_endpoints))))
    table_shape = list(origin_param_var.shape)
    table_shape[0] = zero_dim
    param_var = pserver_program.global_block().create_var(name=origin_param_var.name, shape=table_shape, dtype=origin_param_var.dtype, type=core.VarDesc.VarType.SELECTED_ROWS, persistable=True)
    param_var.desc.set_type(core.VarDesc.VarType.SELECTED_ROWS)
    grad_var = pserver_program.global_block()._clone_variable(self.origin_program.global_block().vars[grad_var_name(self.table_name)])
    table_opt_op = [op for op in self.optimize_ops if (('Param' in op.input_names) and (op.input('Param')[0] == self.table_name))][0]
    table_opt_block = pserver_program.create_block(pre_block_idx)
    if self.sync_mode:
        table_grad_var = self.table_param_grad[1]
        pserver_side_table_grad_list = [pserver_program.global_block().create_var(name=('%s.trainer_%d.pserver_%d' % (table_grad_var.name, index, pserver_index)), type=table_grad_var.type, shape=table_grad_var.shape, dtype=table_grad_var.dtype) for index in range(self.trainer_num)]
        table_opt_block.append_op(type='sum', inputs={
            'X': pserver_side_table_grad_list,
        }, outputs={
            'Out': [grad_var],
        }, attrs={
            'use_mkldnn': False,
        })
    else:
        origin_grad_name = grad_var.name
        splited_grad_name = self.trainer_side_table_grad_list[pserver_index].name
        if (not splited_grad_name.startswith(origin_grad_name)):
            raise ValueError(((('origin_grad_var: ' + splited_grad_name) + ' grad_var:') + grad_var.name))
        grad_var = pserver_program.global_block()._rename_var(origin_grad_name, splited_grad_name)
    lr_var = pserver_program.global_block().vars[table_opt_op.input('LearningRate')[0]]
    inputs = {
        'Param': [param_var],
        'Grad': [grad_var],
        'LearningRate': [lr_var],
    }
    outputs = {
        'ParamOut': [param_var],
    }
    import logging
    logging.warn(("distribute lookup table only support sgd optimizer, change it's optimizer to sgd instead of " + table_opt_op.type))
    table_opt_block.append_op(type='sgd', inputs=inputs, outputs=outputs)
    grad_to_block_id.append(((grad_var.name + ':') + str(table_opt_block.idx)))
    return table_opt_block