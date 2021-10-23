def _get_lr_ops(self):
    lr_ops = []
    lr_vars = set()
    for op in self.optimize_ops:
        if self._is_opt_op(op):
            lr_vars.add(op.input('LearningRate')[0])
    find_ops = []
    block = self.origin_program.global_block()
    for op in block.ops:
        if (set(op.output_arg_names) & lr_vars):
            find_ops.append(op)
    ufind = UnionFind(block.ops)
    for op1 in block.ops:
        for op2 in block.ops:
            if ((op1 != op2) and self._is_op_connected(op1, op2) and (not self._is_opt_op(op1)) and (not self._is_opt_op(op2))):
                ufind.union(op1, op2)
    for op1 in block.ops:
        for op2 in find_ops:
            if ufind.is_connected(op1, op2):
                lr_ops.append(op1)
    return lr_ops