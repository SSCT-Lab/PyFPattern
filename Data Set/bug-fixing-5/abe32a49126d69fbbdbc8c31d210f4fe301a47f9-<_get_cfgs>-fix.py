def _get_cfgs(input_program):
    'Process each block and create ControlFlowGraph for each of them.\n\n    :param input_program: Program object.\n    :return: A list of ControlFlowGraph, each corresponds to a block.\n    '
    ops_list = []
    pdesc = input_program.get_desc()
    block_desc = pdesc.block(0)
    op_size = block_desc.op_size()
    ops_list.extend(_process_sub_block_pair(pdesc, SUB_BLOCK_PAIR))
    skip_opt_set = set()
    for (_, _, skip_opt) in ops_list:
        skip_opt_set.update(skip_opt)
    ops_list.insert(0, ([block_desc.op(i) for i in range(op_size)], op_size, skip_opt_set))
    cfgs = [ControlFlowGraph(input_program, ops, forward_num, skip_opt) for (ops, forward_num, skip_opt) in ops_list]
    return cfgs