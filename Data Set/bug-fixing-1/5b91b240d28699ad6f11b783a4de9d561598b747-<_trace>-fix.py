

def _trace(func, args, return_outs=False, aten=False):
    if isinstance(args, torch.autograd.Variable):
        args = (args,)
    (trace, torch_out) = torch.jit.trace(func, args)
    _optimize_trace(trace, aten)
    if return_outs:
        return (trace, torch_out)
    return trace
