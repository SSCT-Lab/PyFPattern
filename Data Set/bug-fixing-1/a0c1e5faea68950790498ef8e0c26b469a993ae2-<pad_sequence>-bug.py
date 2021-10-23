

def pad_sequence(sequences, batch_first=False, padding_value=0):
    "Pad a list of variable length Tensors with zero\n\n    ``pad_sequence`` stacks a list of Tensors along a new dimension,\n    and padds them to equal length. For example, if the input is list of\n    sequences with size ``L x *`` and if batch_first is False, and ``T x B x *``\n    otherwise. The list of sequences should be sorted in the order of\n    decreasing length.\n\n    `B` is batch size. It's equal to the number of elements in ``sequences``.\n    `T` is length of the longest sequence.\n    `L` is length of the sequence.\n    `*` is any number of trailing dimensions, including none.\n\n    Example:\n        >>> from torch.nn.utils.rnn import pad_sequence\n        >>> a = torch.ones(25, 300)\n        >>> b = torch.ones(22, 300)\n        >>> c = torch.ones(15, 300)\n        >>> pad_sequence([a, b, c]).size()\n        torch.Size([25, 3, 300])\n\n    Note:\n        This function returns a Tensor of size ``T x B x *`` or ``B x T x *`` where `T` is the\n            length of longest sequence.\n        Function assumes trailing dimensions and type of all the Tensors\n            in sequences are same.\n\n    Arguments:\n        sequences (list[Tensor]): list of variable length sequences.\n        batch_first (bool, optional): output will be in ``B x T x *`` if True, or in\n            ``T x B x *`` otherwise\n        padding_value (float, optional): value for padded elements.\n\n    Returns:\n        Tensor of size ``T x B x *`` if batch_first is False\n        Tensor of size ``B x T x *`` otherwise\n    "
    max_size = sequences[0].size()
    (max_len, trailing_dims) = (max_size[0], max_size[1:])
    prev_l = max_len
    if batch_first:
        out_dims = ((len(sequences), max_len) + trailing_dims)
    else:
        out_dims = ((max_len, len(sequences)) + trailing_dims)
    out_tensor = sequences[0].data.new(*out_dims).fill_(padding_value)
    for (i, tensor) in enumerate(sequences):
        length = tensor.size(0)
        if (prev_l < length):
            raise ValueError('lengths array has to be sorted in decreasing order')
        prev_l = length
        if batch_first:
            out_tensor[i, :length, ...] = tensor
        else:
            out_tensor[:length, i, ...] = tensor
    return out_tensor
