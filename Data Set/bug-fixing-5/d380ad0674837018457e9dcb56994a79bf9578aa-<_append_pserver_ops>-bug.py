def _append_pserver_ops(self, program, pserver_program, opt_op, endpoint):
    new_inputs = dict()
    for (key, var) in opt_op.inputs.iteritems():
        if (key == 'Grad'):
            grad_block = None
            for g in self.param_grad_ep_mapping[endpoint]['grads']:
                if g.name.startswith(var.name):
                    grad_block = g
                    break
            if (not grad_block):
                return
            merged_var = program.global_block().create_var(name=grad_block.name, persistable=grad_block.persistable, dtype=grad_block.dtype, shape=grad_block.shape)
            if (self.trainers > 1):
                vars2merge = self._create_var_for_trainers(program.global_block(), grad_block, self.trainers)
                program.global_block().append_op(type='sum', inputs={
                    'X': vars2merge,
                }, outputs={
                    'Out': merged_var,
                })
                program.global_block().append_op(type='scale', inputs={
                    'X': merged_var,
                }, outputs={
                    'Out': merged_var,
                }, attrs={
                    'scale': (1.0 / float(self.trainers)),
                })
            new_inputs[key] = merged_var
        elif (key == 'Param'):
            param_block = None
            for p in self.param_grad_ep_mapping[endpoint]['params']:
                if p.name.startswith(var.name):
                    param_block = p
                    break
            if (not param_block):
                return
            tmpvar = program.global_block().create_var(name=param_block.name, persistable=True, dtype=param_block.dtype, shape=param_block.shape)
            new_inputs[key] = tmpvar
    for (key, var) in opt_op.inputs.iteritems():
        if (key in ['Param', 'Grad']):
            continue
        param_shape = new_inputs['Param'].shape
        new_shape = self._get_optimizer_input_shape(opt_op.type, key, var.shape, param_shape)
        tmpvar = program.global_block().create_var(name=var.name, persistable=var.persistable, dtype=var.dtype, shape=new_shape)
        new_inputs[key] = tmpvar
        pserver_program.global_block().create_var(name=var.name, persistable=var.persistable, dtype=var.dtype, shape=new_shape)
    opt_op.outputs['ParamOut'] = new_inputs['Param']
    program.global_block().append_op(type=opt_op.type, inputs=new_inputs, outputs=opt_op.outputs, attrs=opt_op.attrs)