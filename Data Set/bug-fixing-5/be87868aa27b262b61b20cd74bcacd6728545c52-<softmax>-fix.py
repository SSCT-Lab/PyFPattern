def softmax(x, axis=(- 1)):
    if ((axis == (- 1)) or (axis == (x.ndim - 1))):
        return T.nnet.softmax(x)
    return (T.exp((x - x.max())) / T.exp((x - x.max())).sum(axis=axis, keepdims=True))