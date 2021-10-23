def pad_packed_sequence(sequence, batch_first=False):
    "Pads a packed batch of variable length sequences.\n\n    It is an inverse operation to :func:`pack_padded_sequence`.\n\n    The returned Variable's data will be of size TxBx*, where T is the length\n    of the longest sequence and B is the batch size. If ``batch_size`` is True,\n    the data will be transposed into BxTx* format.\n\n    Batch elements will be ordered decreasingly by their length.\n\n    Arguments:\n        sequence (PackedSequence): batch to pad\n        batch_first (bool, optional): if True, the output will be in BxTx* format.\n\n    Returns:\n        Tuple of Variable containing the padded sequence, and a list of lengths\n        of each sequence in the batch.\n    "
    (var_data, batch_sizes) = sequence
    max_batch_size = batch_sizes[0]
    output = var_data.data.new(len(batch_sizes), max_batch_size, *var_data.size()[1:]).zero_()
    output = Variable(output)
    lengths = []
    data_offset = 0
    prev_batch_size = batch_sizes[0]
    for (i, batch_size) in enumerate(batch_sizes):
        output[i, :batch_size] = var_data[data_offset:(data_offset + batch_size)]
        data_offset += batch_size
        dec = (prev_batch_size - batch_size)
        if (dec > 0):
            lengths.extend(((i,) * dec))
        prev_batch_size = batch_size
    lengths.extend((((i + 1),) * batch_size))
    lengths.reverse()
    if batch_first:
        output = output.transpose(0, 1)
    return (output, lengths)