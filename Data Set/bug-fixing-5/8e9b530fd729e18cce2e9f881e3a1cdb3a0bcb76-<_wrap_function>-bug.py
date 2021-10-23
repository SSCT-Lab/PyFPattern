def _wrap_function(function, ffi):

    @wraps(function)
    def safe_call(*args, **kwargs):
        args = tuple(((ffi.cast((_torch_to_cffi.get(type(arg), 'void') + '*'), arg._cdata) if (torch.is_tensor(arg) or torch.is_storage(arg)) else arg) for arg in args))
        args = ((function,) + args)
        result = torch._C._safe_call(*args, **kwargs)
        if isinstance(result, ffi.CData):
            typeof = ffi.typeof(result)
            if (typeof.kind == 'pointer'):
                cdata = int(ffi.cast('uintptr_t', result))
                cname = typeof.item.cname
                if (cname in _cffi_to_torch):
                    return _cffi_to_torch[cname](cdata=cdata)
        return result
    return safe_call