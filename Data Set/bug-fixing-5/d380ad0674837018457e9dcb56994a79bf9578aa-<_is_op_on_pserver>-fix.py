def _is_op_on_pserver(self, endpoint, all_ops, idx):
    '\n        Recursively check if the op need to run on current server.\n        Assume that ops are in the execution order.\n        '
    param_names = [p.name for p in self.param_grad_ep_mapping[endpoint]['params']]
    op = all_ops[idx]
    if op.inputs.has_key('Param'):
        if (op.inputs['Param'].name in param_names):
            return True
        else:
            for n in param_names:
                if (same_or_split_var(n, op.inputs['Param'].name) and (n != op.inputs['Param'].name)):
                    return True
            return False
    else:
        j = (idx - 1)
        while (j >= 0):
            prev_op = all_ops[j]
            prev_output_names = [o.name for o in prev_op.outputs.values()]
            prev_input_names = [o.name for o in prev_op.inputs.values()]
            found1 = False
            found2 = False
            for (_, v) in op.inputs.iteritems():
                if (v.name in prev_output_names):
                    found1 = self._is_op_on_pserver(endpoint, all_ops, j)
            for (_, v) in op.outputs.iteritems():
                if (v.name in prev_input_names):
                    found2 = self._is_op_on_pserver(endpoint, all_ops, j)
            if (found1 or found2):
                return True
            j -= 1
        return False