

def unchanged_shape(op):
    'Shape function for ops that output a tensor like their first input.'
    return [op.inputs[0].get_shape()]
