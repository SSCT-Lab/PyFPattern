def get_pserver_program(self, endpoint):
    '\n        Get pserver side program using the endpoint.\n        TODO(panyx0718): Revisit this assumption. what if #blocks > #pservers.\n        NOTE: assume blocks of the same variable is not distributed\n        on the same pserver, only change param/grad varnames for\n        trainers to fetch.\n        '
    pserver_program = Program()
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
        if (self.trainers > 1):
            for trainer_id in xrange(self.trainers):
                var = pserver_program.global_block().create_var(name=('%s.trainer_%d' % (orig_var_name, trainer_id)), persistable=False, type=v.type, dtype=v.dtype, shape=v.shape)
                recv_inputs.append(var)
        else:
            recv_inputs.append(single_trainer_var)
    optimize_block = pserver_program.create_block(0)
    ufind = self._create_ufind(self.optimize_ops)
    opt_op_on_pserver = []
    for (_, op) in enumerate(self.optimize_ops):
        if (self._is_opt_op(op) and self._is_opt_op_on_pserver(endpoint, op)):
            opt_op_on_pserver.append(op)
    global_ops = []
    for op in self.optimize_ops:
        if (op.type == 'scale'):
            for in_name in op.input_arg_names:
                if (in_name.startswith('beta1_pow_acc') or in_name.startswith('beta2_pow_acc')):
                    global_ops.append(op)

    def __append_optimize_op__(op, block):
        if self._is_opt_op(op):
            self._append_pserver_ops(block, op, endpoint, default_main_program())
        else:
            self._append_pserver_non_opt_ops(block, op)
    append_block = optimize_block
    lr_ops = self._get_lr_ops()
    if (len(lr_ops) > 0):
        for (_, op) in enumerate(lr_ops):
            self._append_pserver_non_opt_ops(append_block, op)
        append_block = pserver_program.create_block(append_block.idx)
    per_opt_block = append_block
    for (_, opt_op) in enumerate(opt_op_on_pserver):
        for (_, op) in enumerate(self.optimize_ops):
            if (ufind.is_connected(op, opt_op) and (op not in global_ops)):
                __append_optimize_op__(op, per_opt_block)
        per_opt_block = pserver_program.create_block(append_block.idx)
    for glb_op in global_ops:
        __append_optimize_op__(glb_op, per_opt_block)
    pserver_program.global_block().append_op(type='listen_and_serv', inputs={
        'X': recv_inputs,
    }, outputs={
        
    }, attrs={
        'OptimizeBlock': optimize_block,
        'endpoint': endpoint,
        'Fanin': self.trainers,
    })
    pserver_program.sync_with_cpp()
    return pserver_program