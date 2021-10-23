

def squeeze(x, axis):
    'Remove a 1-dimension from the tensor at index "axis".\n    '
    broadcastable = (x.broadcastable[:axis] + x.broadcastable[(axis + 1):])
    x = T.patternbroadcast(x, [(i == axis) for i in range(x.type.ndim)])
    x = T.squeeze(x)
    x = T.patternbroadcast(x, broadcastable)
    return x
