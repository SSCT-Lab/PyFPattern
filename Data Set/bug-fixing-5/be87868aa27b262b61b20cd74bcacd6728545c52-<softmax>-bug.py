def softmax(x, axis=(- 1)):
    if ((axis == (- 1)) or (axis == (x.ndim - 1))):
        return T.nnet.softmax(x)
    return (T.exp(x) / T.exp(x).sum(axis=axis, keepdims=True))