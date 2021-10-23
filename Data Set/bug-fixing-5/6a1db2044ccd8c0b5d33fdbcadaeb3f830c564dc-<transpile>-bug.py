def transpile(self, trainer_id, program=None, pservers='127.0.0.1:6174', trainers=1, sync_mode=True, startup_program=None, current_endpoint='127.0.0.1:6174'):
    '\n        Run the transpiler. Transpile the input program.\n\n        Args:\n            trainer_id (int): id for current trainer worker, if you have\n                n workers, the id may range from 0 ~ n-1\n            program (Program|None): program to transpile,\n                default is fluid.default_main_program().\n            startup_program (Program|None): startup_program to transpile,\n                default is fluid.default_startup_program().\n            pservers (str): comma separated ip:port string for the pserver\n                list.\n            trainers (int|str): in pserver mode this is the number of\n                trainers, in nccl2 mode this is a string of trainer\n                endpoints.\n            sync_mode (bool): Do sync training or not, default is True.\n            startup_program (Program|None): startup_program to transpile,\n                default is fluid.default_main_program().\n            current_endpoint (str): need pass current endpoint when\n                transpile as nccl2 distributed mode. In pserver mode\n                this argument is not used.\n\n        Examples:\n            .. code-block:: python\n\n                transpiler = fluid.DistributeTranspiler()\n                t.transpile(\n                    trainer_id=0,\n                    pservers="127.0.0.1:7000,127.0.0.1:7001",\n                    trainers=2,\n                    sync_mode=False,\n                    current_endpoint="127.0.0.1:7000")\n        '
    if (program is None):
        program = default_main_program()
    if (startup_program is None):
        startup_program = default_startup_program()
    self.origin_program = program
    self.startup_program = startup_program
    self.origin_startup_program = self.startup_program.clone()
    if (self.config.mode == 'nccl2'):
        assert isinstance(trainers, str)
        self.origin_program._trainers_endpoints = trainers.split(',')
        self.origin_program._nccl_comm_num = self.config.nccl_comm_num
        self.origin_program._use_hierarchical_allreduce = self.config.use_hierarchical_allreduce
        if self.config.use_hierarchical_allreduce:
            trainers_num = len(self.origin_program._trainers_endpoints)
            if (self.config.hierarchical_allreduce_inter_nranks <= 1):
                self.config.hierarchical_allreduce_inter_nranks = core.get_cuda_device_count()
            assert (trainers_num > self.config.hierarchical_allreduce_inter_nranks), 'trainers_num:{} < hierarchical_allreduce_inter_nranks:{}'.format(trainers_num, self.config.hierarchical_allreduce_inter_nranks)
            assert ((trainers_num % self.config.hierarchical_allreduce_inter_nranks) == 0), 'trainers_num:{} mod hierarchical_allreduce_inter_nranks:{} != 0'.format(trainers_num, self.config.hierarchical_allreduce_inter_nranks)
            self.origin_program._hierarchical_allreduce_inter_nranks = int(self.config.hierarchical_allreduce_inter_nranks)
        self._transpile_nccl2(trainer_id, trainers, current_endpoint, startup_program=startup_program, wait_port=self.config.wait_port)
        return
    if (self.config.mode == 'collective'):
        self._transpile_collective(collective_mode=self.config.collective_mode, trainer_id=trainer_id, trainers=trainers, current_endpoint=current_endpoint, startup_program=startup_program, main_program=program, wait_port=self.config.wait_port)
        return
    self.trainer_num = trainers
    self.sync_mode = sync_mode
    self.trainer_id = trainer_id
    pserver_endpoints = pservers.split(',')
    self.pserver_endpoints = pserver_endpoints
    self.vars_overview = VarsDistributed()
    (self.optimize_ops, self.params_grads) = self._get_optimize_pass()
    ps_dispatcher = self.config.split_method(self.pserver_endpoints)
    self.table_name = find_distributed_lookup_table(self.origin_program)
    self.has_distributed_lookup_table = (self.table_name != None)
    self.param_name_to_grad_name = dict()
    self.grad_name_to_param_name = dict()
    for (param_var, grad_var) in self.params_grads:
        self.param_name_to_grad_name[param_var.name] = grad_var.name
        self.grad_name_to_param_name[grad_var.name] = param_var.name
    self.sparse_update_ops = self._get_all_remote_sparse_update_op(self.origin_program)
    self.sparse_param_to_height_sections = dict()
    self.origin_program._is_distributed = True
    self.origin_program._endpoints = self.pserver_endpoints
    self.origin_program._ps_endpoint = current_endpoint
    self.origin_program._is_chief = (self.trainer_id == 0)
    self.origin_program._distributed_lookup_table = (self.table_name if self.table_name else None)
    self._init_splited_vars()
    ps_dispatcher.reset()
    send_vars = []
    grad_var_mapping_items = list(six.iteritems(self.grad_var_mapping))
    if (not self.config.slice_var_up):
        np.random.seed(self.origin_program.random_seed)
        np.random.shuffle(grad_var_mapping_items)
    self.grad_name_to_send_dummy_out = dict()
    for (grad_varname, splited_vars) in grad_var_mapping_items:
        eplist = ps_dispatcher.dispatch(splited_vars)
        if (not self.config.slice_var_up):
            assert (len(splited_vars) == 1)
        splited_grad_varname = grad_varname
        if (len(splited_vars) == 1):
            splited_grad_varname = splited_vars[0].name
            index = find_op_by_output_arg(program.global_block(), splited_grad_varname, reverse=True)
        elif (len(splited_vars) > 1):
            orig_var = program.global_block().vars[splited_grad_varname]
            index = find_op_by_output_arg(program.global_block(), splited_grad_varname, reverse=True)
            if (not self.config.runtime_split_send_recv):
                self._insert_split_op(program, orig_var, index, splited_vars)
                index += 1
        else:
            AssertionError('Can not insert the send op by original variable name :', splited_grad_varname)
        if (splited_vars[0].type == core.VarDesc.VarType.SELECTED_ROWS):
            sparse_param_name = self.grad_name_to_param_name[grad_varname]
            if self._is_input_of_remote_sparse_update_op(sparse_param_name):
                self.sparse_param_to_height_sections[sparse_param_name] = [splited_var.shape[0] for splited_var in splited_vars]
        dummy_output = program.global_block().create_var(name=framework.generate_control_dev_var_name())
        self.grad_name_to_send_dummy_out[grad_varname] = dummy_output
        if self.config.runtime_split_send_recv:
            send_input_vars = [program.global_block().vars[splited_grad_varname]]
            sections = self._get_splited_var_sections(splited_vars)
            send_varnames = [var.name for var in splited_vars]
        else:
            send_input_vars = splited_vars
            sections = []
            send_varnames = []
        program.global_block()._insert_op(index=(index + 1), type='send', inputs={
            'X': send_input_vars,
        }, outputs={
            'Out': dummy_output,
        }, attrs={
            'epmap': eplist,
            'sections': sections,
            'send_varnames': send_varnames,
            RPC_OP_ROLE_ATTR_NAME: RPC_OP_ROLE_ATTR_VALUE,
            OP_ROLE_VAR_ATTR_NAME: [self.grad_name_to_param_name[grad_varname], splited_grad_varname],
        })
        for (_, var) in enumerate(splited_vars):
            send_vars.append(var)
    if self.sync_mode:
        send_barrier_out = program.global_block().create_var(name=framework.generate_control_dev_var_name())
        if self.has_distributed_lookup_table:
            self.grad_name_to_send_dummy_out[self.table_name] = program.global_block().create_var(name=framework.generate_control_dev_var_name())
        input_deps = list(self.grad_name_to_send_dummy_out.values())
        program.global_block().append_op(type='send_barrier', inputs={
            'X': list(input_deps),
        }, outputs={
            'Out': send_barrier_out,
        }, attrs={
            'endpoints': pserver_endpoints,
            'trainer_id': self.trainer_id,
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
        distributed_var = self.vars_overview.get_distributed_var_by_slice(recv_vars[i].name)
        distributed_var.endpoint = ep
    all_recv_outputs = []
    for (param_varname, splited_var) in six.iteritems(self.param_var_mapping):
        eps = []
        table_names = []
        for var in splited_var:
            index = [v.name for v in recv_vars].index(var.name)
            eps.append(eplist[index])
            table_names.append(var.name)
        if self.sync_mode:
            recv_dep_in = send_barrier_out
        else:
            recv_dep_in = self.grad_name_to_send_dummy_out[self.param_name_to_grad_name[param_varname]]
        orig_grad_name = self.param_name_to_grad_name[param_varname]
        recv_op_role_var_name = orig_grad_name
        splited_trainer_grad = self.grad_var_mapping[orig_grad_name]
        if (len(splited_trainer_grad) == 1):
            recv_op_role_var_name = splited_trainer_grad[0].name
        if (param_varname in self.sparse_param_to_height_sections):
            for table_name in table_names:
                distributed_var = self.vars_overview.get_distributed_var_by_slice(table_name)
                distributed_var.vtype = 'RemotePrefetch'
            height_sections = self.sparse_param_to_height_sections[param_varname]
            self._update_remote_sparse_update_op(program, param_varname, height_sections, eps, table_names)
        else:
            recv_varnames = []
            if self.config.runtime_split_send_recv:
                orig_param = program.global_block().vars[param_varname]
                recv_varnames = [var.name for var in splited_var]
                splited_var = [orig_param]
            all_recv_outputs.extend(splited_var)
            program.global_block().append_op(type='recv', inputs={
                'X': [recv_dep_in],
            }, outputs={
                'Out': splited_var,
            }, attrs={
                'epmap': eps,
                'recv_varnames': recv_varnames,
                'trainer_id': self.trainer_id,
                RPC_OP_ROLE_ATTR_NAME: RPC_OP_ROLE_ATTR_VALUE,
                OP_ROLE_VAR_ATTR_NAME: [param_varname, recv_op_role_var_name],
            })
    if self.sync_mode:
        program.global_block().append_op(type='fetch_barrier', inputs={
            
        }, outputs={
            'Out': all_recv_outputs,
        }, attrs={
            'endpoints': pserver_endpoints,
            'trainer_id': self.trainer_id,
            RPC_OP_ROLE_ATTR_NAME: RPC_OP_ROLE_ATTR_VALUE,
        })
    for (param_varname, splited_var) in six.iteritems(self.param_var_mapping):
        if (len(splited_var) <= 1):
            continue
        orig_param = program.global_block().vars[param_varname]
        if (param_varname not in self.sparse_param_to_height_sections):
            if (not self.config.runtime_split_send_recv):
                program.global_block().append_op(type='concat', inputs={
                    'X': splited_var,
                }, outputs={
                    'Out': [orig_param],
                }, attrs={
                    'axis': 0,
                    RPC_OP_ROLE_ATTR_NAME: DIST_OP_ROLE_ATTR_VALUE,
                })
    self._get_trainer_startup_program(recv_vars=recv_vars, eplist=eplist)
    if self.has_distributed_lookup_table:
        self._replace_lookup_table_op_with_prefetch(program, pserver_endpoints)
        self._split_table_grad_and_add_send_vars(program, pserver_endpoints)
    self._get_distributed_optimizer_vars()
    self.origin_program._parameters_on_pservers = self.vars_overview