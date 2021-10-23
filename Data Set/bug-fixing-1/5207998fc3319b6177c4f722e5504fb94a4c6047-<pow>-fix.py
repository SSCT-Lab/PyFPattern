

def pow(g, self, exponent):
    return g.op('Pow', self, _if_scalar_type_as(exponent, self), **_broadcast_if_scalar(exponent))
