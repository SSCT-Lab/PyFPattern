def split_dense_variable(var_list, pserver_count, min_block_size=1024, max_block_size=1048576):
    '\n        We may need to split dense tensor to one or several blocks and put\n        them equally onto parameter server. One block is a sub-tensor\n        aligned by dim[0] of the tensor.\n        \n        We need to have a minimal block size so that the calculations in\n        the parameter server side can gain better performance. By default\n        mininum block size is 1024. The max block size is used to prevent\n        too large block that may causing send error.\n    '
    blocks = []
    for var in var_list:
        split_count = pserver_count
        var_numel = reduce((lambda x, y: (x * y)), var.shape)
        max_pserver_count = int(math.floor((var_numel / float(min_block_size))))
        if (max_pserver_count == 0):
            max_pserver_count = 1
        if (max_pserver_count < pserver_count):
            split_count = max_pserver_count
        block_size = int(math.ceil((var_numel / float(split_count))))
        if (len(var.shape) >= 2):
            dim1 = reduce((lambda x, y: (x * y)), var.shape[1:])
            remains = (block_size % dim1)
            if (remains != 0):
                block_size += (dim1 - remains)
        split_count = int(math.ceil((var_numel / float(block_size))))
        for block_id in xrange(split_count):
            curr_block_size = min(block_size, (var_numel - (block_id * block_size)))
            block = VarBlock(var.name, block_id, curr_block_size)
            blocks.append(str(block))
    return blocks