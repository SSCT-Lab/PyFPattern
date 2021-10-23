def _append_pserver_non_opt_ops(self, optimize_block, opt_op):
    program = optimize_block.program
    inputs = self._get_input_map_from_op(self.origin_program.global_block().vars, opt_op)
    for (key, varlist) in six.iteritems(inputs):
        if (not isinstance(varlist, list)):
            varlist = [varlist]
        for i in range(len(varlist)):
            var = varlist[i]
            grad_block = self._get_pserver_grad_param_var(var, program.global_block().vars)
            if grad_block:
                varlist[i] = grad_block
            elif (var.name not in program.global_block().vars):
                tmpvar = program.global_block()._clone_variable(var)
                varlist[i] = tmpvar
            else:
                varlist[i] = program.global_block().vars[var.name]
        inputs[key] = varlist
    outputs = self._get_output_map_from_op(self.origin_program.global_block().vars, opt_op)
    for (key, varlist) in six.iteritems(outputs):
        if (not isinstance(varlist, list)):
            varlist = [varlist]
        for i in range(len(varlist)):
            var = varlist[i]
            grad_block = self._get_pserver_grad_param_var(var, program.global_block().vars)
            if grad_block:
                varlist[i] = grad_block
            elif (var.name not in program.global_block().vars):
                tmpvar = program.global_block()._clone_variable(var)
                varlist[i] = tmpvar
            else:
                varlist[i] = program.global_block().vars[var.name]
        outputs[key] = varlist
    return optimize_block.append_op(type=opt_op.type, inputs=inputs, outputs=outputs, attrs=opt_op.all_attrs())