def forward(self, *args):
    (in_vars, _, _) = _flatten(args)
    module_state = list(self.state_dict(keep_vars=True).values())
    trace = torch._C._tracer_enter((in_vars + module_state), self.nderivs)
    out = self.inner(*args)
    (out_vars, _, _) = _flatten(out)
    torch._C._tracer_exit(out_vars)
    return (trace, out)