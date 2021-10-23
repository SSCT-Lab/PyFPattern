

def pad_sequence(sequences, batch_first=False):
    "Pad a list of variable length Variables with zero\n\n    ``pad_sequence`` stacks a list of Variables along a new dimension,\n    and padds them to equal length. For example, if the input is list of\n    sequences with size ``Lx*`` and if batch_first is False, and ``TxBx*``\n    otherwise. The list of sequences should be sorted in the order of\n    decreasing length.\n\n    B is batch size. It's equal to the number of elements in ``sequences``.\n    T is length longest sequence.\n    L is length of the sequence.\n    * is any number of trailing dimensions, including none.\n\n    Example:\n        >>> from torch.nn.utils.rnn import pad_sequence\n        >>> a = Variable(torch.ones(25, 300))\n        >>> b = Variable(torch.ones(22, 300))\n        >>> c = Variable(torch.ones(15, 300))\n        >>> pad_sequence([a, b, c]).size()\n        torch.Size([25, 3, 300])\n\n    Note:\n        This function returns a Variable of size TxBx* or BxTx* where T is the\n            length of longest sequence.\n        Function assumes trailing dimensions and type of all the Variables\n            in sequences are same.\n\n    Arguments:\n        sequences (list[Variable]): list of variable length sequences.\n        batch_first (bool, optional): output will be in BxTx* if True, or in\n            TxBx* otherwise\n\n    Returns:\n        Variable of size ``T x B x * `` if batch_first is False\n        Variable of size ``B x T x * `` otherwise\n    "
    max_size = sequences[0].size()
    (max_len, trailing_dims) = (max_size[0], max_size[1:])
    prev_l = max_len
    if batch_first:
        out_dims = ((len(sequences), max_len) + trailing_dims)
    else:
        out_dims = ((max_len, len(sequences)) + trailing_dims)
    out_variable = Variable(sequences[0].data.new(*out_dims).zero_())
    for (i, variable) in enumerate(sequences):
        length = variable.size(0)
        if (prev_l < length):
            raise ValueError('lengths array has to be sorted in decreasing order')
        prev_l = length
        if batch_first:
            out_variable[i, :length, ...] = variable
        else:
            out_variable[:length, i, ...] = variable
    return out_variable
