

def get_pserver_program(self, endpoint):
    '\n        Get parameter server side program.\n\n        Args:\n            endpoint (str): current parameter server endpoint.\n\n        Returns:\n            Program: the program for current parameter server to run.\n        '
    pserver_program = Program()
    pserver_program.random_seed = self.origin_program.random_seed
    recv_inputs = []
    for v in self.param_grad_ep_mapping[endpoint]['params']:
        self._clone_var(pserver_program.global_block(), v)
    for v in self.param_grad_ep_mapping[endpoint]['grads']:
        suff_idx = v.name.find('.trainer_')
        if (suff_idx >= 0):
            orig_var_name = v.name[:suff_idx]
        else:
            orig_var_name = v.name
        single_trainer_var = pserver_program.global_block().create_var(name=orig_var_name, persistable=True, type=v.type, dtype=v.dtype, shape=v.shape)
        if (self.sync_mode and (self.trainer_num > 1)):
            for trainer_id in xrange(self.trainer_num):
                var = pserver_program.global_block().create_var(name=('%s.trainer_%d' % (orig_var_name, trainer_id)), persistable=False, type=v.type, dtype=v.dtype, shape=v.shape)
                recv_inputs.append(var)
        else:
            recv_inputs.append(single_trainer_var)
    ufind = self._create_ufind(self.optimize_ops)
    opt_op_on_pserver = []
    for (_, op) in enumerate(self.optimize_ops):
        if (self._is_optimizer_op(op) and self._is_opt_op_on_pserver(endpoint, op)):
            opt_op_on_pserver.append(op)
    global_ops = []

    def __append_optimize_op__(op, block, grad_to_block_id, merged_var, lr_ops):
        if self._is_optimizer_op(op):
            self._append_pserver_ops(block, op, endpoint, grad_to_block_id, self.origin_program, merged_var)
        elif (op not in lr_ops):
            self._append_pserver_non_opt_ops(block, op)

    def __op_have_grad_input__(op):
        for varname in op.input_arg_names:
            if (varname.find('@GRAD') >= 0):
                return varname
        return ''

    def __clone_lr_op_sub_block__(op, program, lr_block):
        if (not op.has_attr('sub_block')):
            return
        origin_block_desc = op.attr('sub_block')
        origin_block = self.origin_program.block(origin_block_desc.id)
        assert isinstance(origin_block, Block)
        new_sub_block = program.create_block(lr_block.idx)
        for var in origin_block.vars:
            new_sub_block._clone_variable(var)
        for origin_op in origin_block.ops:
            cloned_op = self._clone_lr_op(program, new_sub_block, origin_op)
            __clone_lr_op_sub_block__(cloned_op, program, new_sub_block)
        op.set_attr('sub_block', new_sub_block)
    lr_ops = self._get_lr_ops()
    optimize_blocks = []
    if (len(lr_ops) > 0):
        lr_decay_block = pserver_program.create_block((pserver_program.num_blocks - 1))
        optimize_blocks.append(lr_decay_block)
        for (_, op) in enumerate(lr_ops):
            cloned_op = self._append_pserver_non_opt_ops(lr_decay_block, op)
            __clone_lr_op_sub_block__(cloned_op, pserver_program, lr_decay_block)
    grad_to_block_id = []
    pre_block_idx = (pserver_program.num_blocks - 1)
    for (idx, opt_op) in enumerate(opt_op_on_pserver):
        per_opt_block = pserver_program.create_block(pre_block_idx)
        optimize_blocks.append(per_opt_block)
        for (_, op) in enumerate(self.optimize_ops):
            grad_varname_for_block = __op_have_grad_input__(op)
            if (ufind.is_connected(op, opt_op) and grad_varname_for_block):
                merged_var = self._append_pserver_grad_merge_ops(per_opt_block, grad_varname_for_block, endpoint, grad_to_block_id, self.origin_program)
                break
        for (_, op) in enumerate(self.optimize_ops):
            if (ufind.is_connected(op, opt_op) and (op not in global_ops)):
                __append_optimize_op__(op, per_opt_block, grad_to_block_id, merged_var, lr_ops)
    grad_to_block_id = list(set(grad_to_block_id))
    if global_ops:
        opt_state_block = pserver_program.create_block((pserver_program.num_blocks - 1))
        optimize_blocks.append(opt_state_block)
        for glb_op in global_ops:
            __append_optimize_op__(glb_op, opt_state_block, grad_to_block_id, None, lr_ops)
    prefetch_var_name_to_block_id = []
    if self.has_distributed_lookup_table:
        pserver_index = self.pserver_endpoints.index(endpoint)
        table_opt_block = self._create_table_optimize_block(pserver_index, pserver_program, pre_block_idx, grad_to_block_id)
        prefetch_var_name_to_block_id = self._create_prefetch_block(pserver_index, pserver_program, table_opt_block)
        checkpoint_block_id = self._create_checkpoint_save_block(pserver_program, table_opt_block.idx)
    if self.has_distributed_lookup_table:
        assert (len(prefetch_var_name_to_block_id) > 0)
    else:
        assert (len(prefetch_var_name_to_block_id) == 0)
    attrs = {
        'optimize_blocks': optimize_blocks,
        'endpoint': endpoint,
        'Fanin': self.trainer_num,
        'sync_mode': self.sync_mode,
        'grad_to_block_id': grad_to_block_id,
    }
    if (len(prefetch_var_name_to_block_id) > 0):
        attrs['prefetch_var_name_to_block_id'] = prefetch_var_name_to_block_id
        attrs['checkpint_block_id'] = checkpoint_block_id
    pserver_program.global_block().append_op(type='listen_and_serv', inputs={
        'X': recv_inputs,
    }, outputs={
        
    }, attrs=attrs)
    pserver_program._sync_with_cpp()
    return pserver_program
