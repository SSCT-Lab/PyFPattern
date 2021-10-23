

def pack_padded_sequence(input, lengths, batch_first=False):
    'Packs a Variable containing padded sequences of variable length.\n\n    Input can be of size ``TxBx*`` where T is the length of the longest sequence\n    (equal to ``lengths[0]``), B is the batch size, and * is any number of\n    dimensions (including 0). If ``batch_first`` is True ``BxTx*`` inputs are\n    expected.\n\n    The sequences should be sorted by length in a decreasing order, i.e.\n    ``input[:,0]`` should be the longest sequence, and ``input[:,B-1]`` the\n    shortest one.\n\n    Note:\n        This function accept any input that has at least two dimensions. You\n        can apply it to pack the labels, and use the output of the RNN with\n        them to compute the loss directly. A Variable can be retrieved from\n        a :class:`PackedSequence` object by accessing its ``.data`` attribute.\n\n    Arguments:\n        input (Variable): padded batch of variable length sequences.\n        lengths (list[int]): list of sequences lengths of each batch element.\n        batch_first (bool, optional): if True, the input is expected in BxTx*\n            format.\n\n    Returns:\n        a :class:`PackedSequence` object\n    '
    if (lengths[(- 1)] <= 0):
        raise ValueError("length of all samples has to be greater than 0, but found an element in 'lengths' that is <=0")
    if batch_first:
        input = input.transpose(0, 1)
    steps = []
    batch_sizes = []
    lengths_iter = reversed(lengths)
    batch_size = input.size(1)
    if (len(lengths) != batch_size):
        raise ValueError('lengths array has incorrect size')
    prev_l = 0
    for (i, l) in enumerate(lengths_iter):
        if (l > prev_l):
            c_batch_size = (batch_size - i)
            steps.append(input[prev_l:l, :c_batch_size].contiguous().view((- 1), input.size(2)))
            batch_sizes.extend(([c_batch_size] * (l - prev_l)))
            prev_l = l
        elif (prev_l > l):
            raise ValueError('lengths array has to be sorted in decreasing order')
    return PackedSequence(torch.cat(steps), batch_sizes)
