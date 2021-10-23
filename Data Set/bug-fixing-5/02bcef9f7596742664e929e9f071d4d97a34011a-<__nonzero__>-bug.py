def __nonzero__(self):
    msg = "Don't convert Expr to bool. Please call Expr.eval method to evaluate expression."
    raise RuntimeError(msg)