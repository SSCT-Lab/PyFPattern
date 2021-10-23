def _append_pserver_non_opt_ops(self, optimize_block, opt_op):
    program = optimize_block.program
    inputs = self._get_input_map_from_op(self.origin_program.global_block().vars, opt_op)
    for (key, varlist) in six.iteritems(inputs):
        if (not isinstance(varlist, list)):
            varlist = [varlist]
        for var in varlist:
            grad_block = self._is_splited_grad_var(var, program.global_block().vars)
            if grad_block:
                inputs[key] = grad_block
            elif (var.name not in program.global_block().vars):
                program.global_block().create_var(name=var.name, persistable=var.persistable, dtype=var.dtype, shape=var.shape)
    outputs = self._get_output_map_from_op(self.origin_program.global_block().vars, opt_op)
    for (key, varlist) in six.iteritems(outputs):
        if (not isinstance(varlist, list)):
            varlist = [varlist]
        for var in varlist:
            grad_block = self._is_splited_grad_var(var, program.global_block().vars)
            if grad_block:
                outputs[key] = grad_block
            elif (var.name not in program.global_block().vars):
                program.global_block()._clone_variable(var)
    return optimize_block.append_op(type=opt_op.type, inputs=inputs, outputs=outputs, attrs=opt_op.all_attrs())