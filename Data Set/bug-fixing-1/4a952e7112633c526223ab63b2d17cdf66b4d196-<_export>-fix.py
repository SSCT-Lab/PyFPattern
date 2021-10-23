

def _export(model, args, f, export_params=True, kwargs=None, verbose=False):
    if isinstance(args, torch.autograd.Variable):
        args = (args,)
    if (not kwargs):
        kwargs = {
            
        }
    (trace, torch_out) = torch.jit.record_trace(model, *args, **kwargs)
    if export_params:
        proto = trace.export(list(model.state_dict().values()), verbose)
    else:
        proto = trace.export(verbose)
    torch.serialization._with_file_like(f, 'wb', (lambda f: f.write(proto)))
    return torch_out
