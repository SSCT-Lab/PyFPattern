def _l2norm(self, v):
    'inner product implementation'
    norm = multiply(v, v).asnumpy().sum()
    return norm