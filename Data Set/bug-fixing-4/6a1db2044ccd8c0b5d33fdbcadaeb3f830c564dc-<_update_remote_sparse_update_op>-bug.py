def _update_remote_sparse_update_op(self, program, param_varname, height_sections, endpoints, table_names):
    ops = []
    op_type = ''
    for op in self.sparse_update_ops:
        if ((param_varname in op.input_arg_names) and (op_type == '')):
            op_type = op.type
            ops.append(op)
        elif ((param_varname in op.input_arg_names) and (op_type == op.type)):
            ops.append(op)
    if (op_type == 'lookup_table'):
        all_ops = program.global_block().ops
        op_idxs = [all_ops.index(op) for op in ops]
        inputs = [program.global_block().vars[op.input('Ids')[0]] for op in ops]
        w = program.global_block().vars[ops[0].input('W')[0]]
        padding_idx = ops[0].attr('padding_idx')
        outputs = [program.global_block().vars[op.output('Out')[0]] for op in ops]
        for idx in op_idxs[::(- 1)]:
            program.global_block()._remove_op(idx)
        program.global_block()._insert_op(index=op_idxs[0], type='distributed_lookup_table', inputs={
            'Ids': inputs,
            'W': w,
        }, outputs={
            'Outputs': outputs,
        }, attrs={
            'table_names': table_names,
            'height_sections': height_sections,
            'endpoints': endpoints,
            'padding_idx': padding_idx,
            'trainer_id': self.trainer_id,
        })