def squeeze(x, axis):
    'Remove a 1-dimension from the tensor at index "axis".\n    '
    shape = list(x.shape)
    shape.pop(axis)
    return T.reshape(x, tuple(shape))