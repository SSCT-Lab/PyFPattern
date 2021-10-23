def _update_remote_sparse_update_op(self, program, need_sparse_update_params):
    for (param_varname, attrs) in need_sparse_update_params.items():
        height_sections = self.sparse_param_to_height_sections[param_varname]
        endpoints = attrs[0]
        table_names = attrs[1]
        ops = []
        op_type = ''
        used_ops = []
        for (idx, op) in enumerate(self.sparse_update_ops):
            if ((param_varname in op.input_arg_names) and (op_type == '')):
                op_type = op.type
                ops.append(op)
                used_ops.append(idx)
            elif ((param_varname in op.input_arg_names) and (op_type == op.type)):
                ops.append(op)
                used_ops.append(idx)
        if (op_type == 'lookup_table'):
            all_ops = program.global_block().ops
            op_idxs = [all_ops.index(op) for op in ops]
            inputs = [program.global_block().vars[op.input('Ids')[0]] for op in ops]
            w = program.global_block().vars[ops[0].input('W')[0]]
            padding_idx = ops[0].attr('padding_idx')
            outputs = [program.global_block().vars[op.output('Out')[0]] for op in ops]
            for idx in op_idxs[::(- 1)]:
                program.global_block()._remove_op(idx)
            inputs_idxs = ([(- 1)] * len(inputs))
            outputs_idxs = ([(- 1)] * len(outputs))
            for (idx, op) in enumerate(program.global_block().ops):
                for i in range(0, len(op.output_names)):
                    outs = op.output(op.output_names[i])
                    for (in_id, in_var) in enumerate(inputs):
                        if (in_var.name in outs):
                            inputs_idxs[in_id] = idx
                for i in range(0, len(op.input_names)):
                    ins = op.input(op.input_names[i])
                    for (out_id, out_var) in enumerate(outputs):
                        if (out_var.name in ins):
                            outputs_idxs[out_id] = idx
            if ((min(outputs_idxs) - max(inputs_idxs)) >= 1):
                distributed_idx = (max(inputs_idxs) + 1)
                program.global_block()._insert_op(index=distributed_idx, type='distributed_lookup_table', inputs={
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
            else:
                raise ValueError('something wrong with distribute_transpiler, submit a issue is recommended')
            for idx in used_ops[::(- 1)]:
                self.sparse_update_ops.pop(idx)