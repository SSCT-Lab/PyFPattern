def _process_sub_block_pair(pdesc, sub_block_pair):
    "Creates a list of tuple each of which tracks info of a subblock.\n\n      Note: this function doesn't handle nested subblocks yet.\n      TODO(panyx0718): assert if case nested subblocks happen.\n\n    :param pdesc: ProgramDesc.\n    :param sub_block_pair: A list op pairs. Each op pair is the forward\n        op and backward op. The ops in the list are special that they contain\n        a subblock of ops.\n    :return: A list of tuples, each tuple is (all ops in a subblock pair\n        including forward and backward, number of forward ops,\n        all output args names of the ops in the subblock pairs).\n    "
    ops_list = []
    block_desc = pdesc.block(0)
    op_size = block_desc.op_size()
    for (fwd_op, bwd_op) in sub_block_pair:
        sub_block_ids = []
        grad_sub_block_ids = []
        sub_block_id_pair = []
        sub_op_dict = {
            
        }
        for i in range(op_size):
            op = block_desc.op(i)
            if (op.type() == fwd_op):
                sub_block_ids.append(op.attr('sub_block').id)
                sub_op_dict[op.attr('sub_block').id] = op
            elif (op.type() == bwd_op):
                grad_sub_block_ids.append(op.attr('sub_block').id)
                sub_op_dict[op.attr('sub_block').id] = op
        for grad_id in grad_sub_block_ids:
            fwd_id = pdesc.block(grad_id).get_forward_block_idx()
            if (fwd_id in sub_block_ids):
                sub_block_id_pair.append((fwd_id, grad_id))
                sub_block_ids.remove(fwd_id)
        for (fwd_id, grad_id) in sub_block_id_pair:
            sub_block_ops = []
            sub_block = pdesc.block(fwd_id)
            block_op_size = sub_block.op_size()
            for i in range(block_op_size):
                sub_block_ops.append(sub_block.op(i))
            grad_sub_block = pdesc.block(grad_id)
            grad_sub_block_op_size = grad_sub_block.op_size()
            for i in range(grad_sub_block_op_size):
                sub_block_ops.append(grad_sub_block.op(i))
            sub_op_output = set()
            sub_op_output.update(sub_op_dict[fwd_id].output_arg_names())
            sub_op_output.update(sub_op_dict[grad_id].output_arg_names())
            sub_op_output.update(sub_op_dict[fwd_id].input_arg_names())
            sub_op_output.update(sub_op_dict[grad_id].input_arg_names())
            ops_list.append((sub_block_ops, block_op_size, sub_op_output))
        for fwd_id in sub_block_ids:
            sub_block_ops = []
            sub_block = pdesc.block(fwd_id)
            sub_block_op_size = sub_block.op_size()
            for i in range(sub_block_op_size):
                sub_block_ops.append(sub_block.op(i))
            sub_op_output = set()
            sub_op_output.update(sub_op_dict[fwd_id].output_arg_names())
            sub_op_output.update(sub_op_dict[fwd_id].input_arg_names())
            ops_list.append((sub_block_ops, sub_block_op_size, sub_op_output))
    return ops_list