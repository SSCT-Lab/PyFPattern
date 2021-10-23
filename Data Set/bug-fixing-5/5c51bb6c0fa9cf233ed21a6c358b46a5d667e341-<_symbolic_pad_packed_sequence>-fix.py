def _symbolic_pad_packed_sequence(g, input, batch_first=False, padding_value=0.0):
    (data, lengths) = g.op('PadPacked', input.data, input.batch_sizes, outputs=2)
    if batch_first:
        data = g.op('Transpose', data, perm_i=[1, 0, 2])
    return (data, lengths)