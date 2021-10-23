def _symbolic_pack_padded_sequence(g, input, lengths, batch_first=False):
    if batch_first:
        from torch.onnx import symbolic
        input = symbolic.t(g, input)
    return g.op('PackPadded', input, lengths, outputs=2)