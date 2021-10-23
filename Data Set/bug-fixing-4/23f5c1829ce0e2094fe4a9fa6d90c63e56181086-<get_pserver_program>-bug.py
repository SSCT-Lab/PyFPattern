def get_pserver_program(self, endpoint):
    '\n        get pserver side program by endpoint\n\n        NOTE: assume blocks of the same variable is not distributed\n        on the same pserver, only change param/grad varnames for\n        trainers to fetch. For each pserver endpoint, server side\n        program must be a sub-set of the original optimization program.\n        '
    pserver_program = Program()
    for v in self.param_grad_ep_mapping[endpoint]['params']:
        self._clone_var(pserver_program.global_block(), v)
    for v in self.param_grad_ep_mapping[endpoint]['grads']:
        pserver_program.global_block().create_var(name=v.name, persistable=True, dtype=v.dtype, shape=v.shape)
        for trainer_id in xrange(self.trainers):
            print(('create variable for program: %s.trainer_%d' % (v.name, trainer_id)))
            pserver_program.global_block().create_var(name=('%s.trainer_%d' % (v.name, trainer_id)), persistable=True, dtype=v.dtype, shape=v.shape)
    optimize_sub_program = Program()
    for (idx, opt_op) in enumerate(self.optimize_ops):
        is_op_on_pserver = self._is_op_on_pserver(endpoint, self.optimize_ops, idx)
        if (not is_op_on_pserver):
            continue
        if opt_op.inputs.has_key('Grad'):
            self._append_pserver_ops(optimize_sub_program, pserver_program, opt_op, endpoint)
        else:
            self._append_pserver_non_opt_ops(optimize_sub_program, pserver_program, opt_op)
    pserver_program.global_block().append_op(type='recv', inputs={
        'RX': self.param_grad_ep_mapping[endpoint]['grads'],
    }, outputs={
        
    }, attrs={
        'OptimizeBlock': optimize_sub_program.global_block(),
        'endpoint': endpoint,
        'ParamList': [p.name for p in self.param_grad_ep_mapping[endpoint]['params']],
        'GradList': [p.name for p in self.param_grad_ep_mapping[endpoint]['grads']],
        'Fanin': self.trainers,
    })
    pserver_program.sync_with_cpp()
    return pserver_program