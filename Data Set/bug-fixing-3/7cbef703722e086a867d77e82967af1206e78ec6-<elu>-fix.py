def elu(g, input, alpha, scale):
    if (scale and (scale != 1.0)):
        return _unimplemented('scale', 'does not support scale in Elu')
    return g.op('Elu', input, alpha_f=_scalar(alpha))