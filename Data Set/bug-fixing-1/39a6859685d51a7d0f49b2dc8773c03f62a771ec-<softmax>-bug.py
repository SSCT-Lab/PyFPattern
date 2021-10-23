

def softmax(g, input, dim=None):
    if (dim < 0):
        check_dim = (len(input.type().sizes()) + dim)
    if (len(input.type().sizes()) != (check_dim + 1)):
        return _unimplemented('dim', 'ONNX and PyTorch use different strategies to split the input.')
    return g.op('Softmax', input, axis_i=dim)
