def _symbolic_pack_padded_sequence(g, input, lengths, batch_first=False):
    if batch_first:
        input = g.op('Transpose', input, perm_i=[1, 0, 2])
    return g.op('PackPadded', input, lengths, outputs=2)