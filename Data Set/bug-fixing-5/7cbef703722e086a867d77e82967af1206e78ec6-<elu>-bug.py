def elu(g, input, alpha, inplace=False):
    return g.op('Elu', input, alpha_f=_scalar(alpha))