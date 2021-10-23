def get_startup_program(self, endpoint, pserver_program):
    '\n        Get startup program for current parameter server.\n        Modify operator input variables if there are variables that\n        were split to several blocks.\n        '
    s_prog = Program()
    orig_s_prog = framework.default_startup_program()
    params = self.param_grad_ep_mapping[endpoint]['params']

    def _get_splited_name_and_shape(varname):
        for (idx, splited_param) in enumerate(params):
            pname = splited_param.name
            if (same_or_split_var(pname, varname) and (varname != pname)):
                return (pname, splited_param.shape)
        return ('', [])
    pserver_vars = pserver_program.global_block().vars
    created_var_map = dict()
    for (_, var) in pserver_vars.iteritems():
        tmpvar = s_prog.global_block().create_var(name=var.name, persistable=var.persistable, dtype=var.dtype, shape=var.shape)
        created_var_map[var.name] = tmpvar
    for op in orig_s_prog.global_block().ops:
        new_outputs = dict()
        op_on_pserver = False
        for (key, var) in op.outputs.iteritems():
            (newname, _) = _get_splited_name_and_shape(var.name)
            if newname:
                op_on_pserver = True
                new_outputs[key] = created_var_map[newname]
            elif (var.name in pserver_vars):
                op_on_pserver = True
                new_outputs[key] = pserver_vars[var.name]
        if op_on_pserver:
            if (op.type in ['gaussian_random', 'fill_constant', 'uniform_random']):
                op.attrs['shape'] = new_outputs['Out'].shape
            s_prog.global_block().append_op(type=op.type, inputs=op.inputs, outputs=new_outputs, attrs=op.attrs)
    return s_prog