

def __nonzero__(self):
    msg = 'An Expr instance cannot be evaluated as bool. Please use chainer.type_check.eval() to evaluate an expression.'
    raise RuntimeError(msg)
