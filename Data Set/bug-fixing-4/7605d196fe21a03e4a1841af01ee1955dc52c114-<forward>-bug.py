def forward(self, *args):
    (in_vars, _, _) = _flatten((args, list(self.parameters())))
    return _get_trace(self.inner, args, in_vars, self.nderivs)