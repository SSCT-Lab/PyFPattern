

def _split_table_grad_and_add_send_vars(self, program, pserver_endpoints):
    all_ops = program.global_block().ops
    table_grad_name = grad_var_name(self.table_name)
    for op in all_ops:
        if (table_grad_name in op.output_arg_names):
            op_index = list(all_ops).index(op)
            program.global_block()._insert_op(index=(op_index + 1), type='split_ids', inputs={
                'Ids': [program.global_block().vars[table_grad_name]],
            }, outputs={
                'Out': self.trainer_side_table_grad_list,
            })
            program.global_block()._insert_op(index=(op_index + 2), type='send', inputs={
                'X': self.trainer_side_table_grad_list,
            }, outputs={
                'Out': ([self.grad_name_to_send_dummy_out[self.table_name]] if self.sync_mode else []),
            }, attrs={
                'sync_mode': self.sync_mode,
                'epmap': pserver_endpoints,
                RPC_OP_ROLE_ATTR_NAME: RPC_OP_ROLE_ATTR_VALUE,
                OP_ROLE_VAR_ATTR_NAME: [self.grad_name_to_param_name[table_grad_name], table_grad_name],
            })
            break
