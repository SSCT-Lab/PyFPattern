

def instance_norm(g, input, **kwargs):
    input_type = input.type().scalarType()
    weight = kwargs.get('weight', None)
    bias = kwargs.get('bias', None)
    eps = kwargs.get('eps', 1e-05)
    if (not weight):
        weight = g.constant(1.0, [input.type().sizes()[1]], input_type)
    else:
        weight = g.op('Constant', value_t=weight)
    if (not bias):
        bias = g.constant(0.0, [input.type().sizes()[1]], input_type)
    else:
        bias = g.op('Constant', value_t=bias)
    return g.op('InstanceNormalization', input, weight, bias, epsilon_f=eps)
