def transpile(self, trainer_id, program=None, pservers='127.0.0.1:6174', trainers=1, slice_var_up=True, split_method=RoundRobin, sync_mode=True):
    '\n        Run the transpiler.\n\n        Args:\n            trainer_id (int): id for current trainer worker, if you have\n                n workers, the id may range from 0 ~ n-1\n            program (Program|None): program to transpile,\n                default is fluid.default_main_program().\n            pservers (str): comma separated ip:port string for the pserver\n                list.\n            trainers (int): number of trainers in the distributed job.\n            slice_var_up (bool): Do Tensor slice for pservers, default is True.\n            split_method (PSDispatcher): RoundRobin or HashName can be used\n                try to choose the best method to balance loads for pservers.\n            sync_mode (bool): Do sync training or not, default is True.\n        '
    assert (split_method.__bases__[0] == PSDispatcher)
    if (program is None):
        program = default_main_program()
    self.origin_program = program
    self.trainer_num = trainers
    self.sync_mode = sync_mode
    self.trainer_id = trainer_id
    pserver_endpoints = pservers.split(',')
    self.pserver_endpoints = pserver_endpoints
    (self.optimize_ops, self.params_grads) = self._get_optimize_pass()
    ps_dispatcher = split_method(self.pserver_endpoints)
    self.has_distributed_lookup_table = self._has_distributed_lookup_table()
    self._init_splited_vars(slice_var_up)
    ps_dispatcher.reset()
    send_vars = []
    grad_var_mapping_items = self.grad_var_mapping.items()
    if (not slice_var_up):
        np.random.shuffle(grad_var_mapping_items)
    for (orig_varname, splited_vars) in grad_var_mapping_items:
        eplist = ps_dispatcher.dispatch(splited_vars)
        if (not slice_var_up):
            assert (len(splited_vars) == 1)
        if (len(splited_vars) == 1):
            orig_varname = splited_vars[0].name
            index = find_op_by_output_arg(program.global_block(), orig_varname)
        elif (len(splited_vars) > 1):
            orig_var = program.global_block().vars[orig_varname]
            index = find_op_by_output_arg(program.global_block(), orig_varname)
            self._insert_split_op(program, orig_var, index, splited_vars)
            index += 1
        else:
            AssertionError('Can not insert the send op by original variable name :', orig_varname)
        program.global_block().insert_op(index=(index + 1), type='send', inputs={
            'X': splited_vars,
        }, outputs={
            
        }, attrs={
            'epmap': eplist,
            RPC_OP_ROLE_ATTR_NAME: RPC_OP_ROLE_ATTR_VALUE,
        })
        for (_, var) in enumerate(splited_vars):
            send_vars.append(var)
    if self.sync_mode:
        program.global_block().append_op(type='send_barrier', inputs={
            
        }, outputs={
            
        }, attrs={
            'endpoints': pserver_endpoints,
            'sync_mode': self.sync_mode,
            RPC_OP_ROLE_ATTR_NAME: RPC_OP_ROLE_ATTR_VALUE,
        })
    recv_vars = []
    for (_, var) in enumerate(send_vars):
        recv_vars.append(self.grad_param_mapping[var])
    ps_dispatcher.reset()
    eplist = ps_dispatcher.dispatch(recv_vars)
    for (i, ep) in enumerate(eplist):
        self.param_grad_ep_mapping[ep]['params'].append(recv_vars[i])
        self.param_grad_ep_mapping[ep]['grads'].append(send_vars[i])
    for (varname, splited_var) in self.param_var_mapping.iteritems():
        eps = []
        for var in splited_var:
            index = [v.name for v in recv_vars].index(var.name)
            eps.append(eplist[index])
        program.global_block().append_op(type='recv', inputs={
            
        }, outputs={
            'Out': splited_var,
        }, attrs={
            'epmap': eps,
            RPC_OP_ROLE_ATTR_NAME: RPC_OP_ROLE_ATTR_VALUE,
        })
    program.global_block().append_op(type='fetch_barrier', inputs={
        
    }, outputs={
        
    }, attrs={
        'endpoints': pserver_endpoints,
        RPC_OP_ROLE_ATTR_NAME: RPC_OP_ROLE_ATTR_VALUE,
    })
    for (varname, splited_var) in self.param_var_mapping.iteritems():
        if (len(splited_var) <= 1):
            continue
        orig_param = program.global_block().vars[varname]
        program.global_block().append_op(type='concat', inputs={
            'X': splited_var,
        }, outputs={
            'Out': [orig_param],
        }, attrs={
            'axis': 0,
        })
    if self.has_distributed_lookup_table:
        self._replace_lookup_table_op_with_prefetch(program, pserver_endpoints)
        self._split_table_grad_and_add_send_vars(program, pserver_endpoints)