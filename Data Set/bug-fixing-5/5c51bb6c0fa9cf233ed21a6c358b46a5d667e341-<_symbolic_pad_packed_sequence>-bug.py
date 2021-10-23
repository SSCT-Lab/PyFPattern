def _symbolic_pad_packed_sequence(g, input, batch_first=False, padding_value=0.0):
    (data, lengths) = g.op('PadPacked', input.data, input.batch_sizes, outputs=2)
    if batch_first:
        from torch.onnx import symbolic
        data = symbolic.t(g, data)
    return (data, lengths)