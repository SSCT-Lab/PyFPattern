def _update_dist_lookup_table_vars(self, param_list, grad_list, params_grads):
    program = self.origin_program
    if self.has_distributed_lookup_table:
        param_list = [param for param in param_list if (param.name != self.table_name)]
        grad_list = [grad for grad in grad_list if (grad.name != grad_var_name(self.table_name))]
        self.table_param_grad = [param_grad for param_grad in params_grads if (param_grad[0].name == self.table_name)][0]
        table_grad_var = self.table_param_grad[1]
        if self.sync_mode:
            self.trainer_side_table_grad_list = [program.global_block().create_var(name=('%s.trainer_%d.pserver_%d' % (table_grad_var.name, self.trainer_id, index)), type=table_grad_var.type, shape=table_grad_var.shape, dtype=table_grad_var.dtype) for index in range(len(self.pserver_endpoints))]
        else:
            self.trainer_side_table_grad_list = [program.global_block().create_var(name=('%s.pserver_%d' % (table_grad_var.name, index)), type=table_grad_var.type, shape=table_grad_var.shape, dtype=table_grad_var.dtype) for index in range(len(self.pserver_endpoints))]