def CosineLoss(a, b, label):
    a = mx.symbol.L2Normalization(a)
    b = mx.symbol.L2Normalization(b)
    dot = (a * b)
    dot = mx.symbol.sum_axis(dot, axis=1)
    dot = mx.symbol.Flatten(dot)
    cosine = (1 - dot)
    return mx.symbol.MAERegressionOutput(data=cosine, label=label)