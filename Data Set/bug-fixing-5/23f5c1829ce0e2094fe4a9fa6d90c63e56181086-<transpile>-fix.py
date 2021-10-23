def transpile(self, optimize_ops, params_grads, program=None, pservers='127.0.0.1:6174', trainers=1, split_method=round_robin):
    '\n            Transpile the program to distributed data-parallelism programs.\n            The main_program will be transformed to use a remote parameter server\n            to do parameter optimization. And the optimization graph will be put\n            into a parameter server program.\n\n            Use different methods to split trainable variables to different\n            parameter servers.\n\n            :param optimize_ops: op list of optimization, should be the\n                                 return value of Optimizer.minimize\n            :type optimize_ops: list\n            :param program: program to optimize, default is default_main_program\n            :param pservers: parameter server endpoints like "m1:6174,m2:6174"\n            :type pservers: string\n            :return: return a list of programs\n        '
    assert callable(split_method)
    if (program is None):
        program = default_main_program()
    self.program = program
    self.trainers = trainers
    self.optimize_ops = optimize_ops
    pserver_endpoints = pservers.split(',')
    param_list = [pg[0] for pg in params_grads]
    grad_list = [pg[1] for pg in params_grads]
    grad_blocks = split_dense_variable(grad_list, len(pserver_endpoints))
    param_blocks = split_dense_variable(param_list, len(pserver_endpoints))
    grad_var_mapping = self._append_split_op(program, grad_blocks)
    send_inputs = []
    send_outputs = []
    for b in grad_blocks:
        (varname, block_id, _) = b.split(':')
        send_inputs.append(grad_var_mapping[varname][int(block_id)])
    param_var_mapping = self._create_vars_from_blocklist(program, param_blocks)
    for b in param_blocks:
        (varname, block_id, _) = b.split(':')
        send_outputs.append(param_var_mapping[varname][int(block_id)])
    eplist = split_method(send_inputs, pserver_endpoints)
    self.param_grad_ep_mapping = dict()
    for (i, ep) in enumerate(eplist):
        param = send_outputs[i]
        grad = send_inputs[i]
        if (not self.param_grad_ep_mapping.has_key(ep)):
            self.param_grad_ep_mapping[ep] = {
                'params': [],
                'grads': [],
            }
        self.param_grad_ep_mapping[ep]['params'].append(param)
        self.param_grad_ep_mapping[ep]['grads'].append(grad)
    send_op = program.global_block().append_op(type='send', inputs={
        'X': send_inputs,
    }, outputs={
        'Out': send_outputs,
    }, attrs={
        'endpoints': pserver_endpoints,
        'epmap': eplist,
    })
    for (varname, splited_var) in param_var_mapping.iteritems():
        if (len(splited_var) <= 1):
            continue
        orig_param = program.global_block().vars[varname]
        concat = program.global_block().append_op(type='concat', inputs={
            'X': splited_var,
        }, outputs={
            'Out': [orig_param],
        }, attrs={
            'axis': 0,
        })