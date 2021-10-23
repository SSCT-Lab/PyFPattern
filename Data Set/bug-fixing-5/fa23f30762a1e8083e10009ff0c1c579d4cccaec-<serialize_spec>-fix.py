def serialize_spec(clonespec):
    'Serialize a clonespec or a relocation spec'
    data = {
        
    }
    attrs = dir(clonespec)
    attrs = [x for x in attrs if (not x.startswith('_'))]
    for x in attrs:
        xo = getattr(clonespec, x)
        if callable(xo):
            continue
        xt = type(xo)
        if (xo is None):
            data[x] = None
        elif isinstance(xo, vim.vm.ConfigSpec):
            data[x] = serialize_spec(xo)
        elif isinstance(xo, vim.vm.RelocateSpec):
            data[x] = serialize_spec(xo)
        elif isinstance(xo, vim.vm.device.VirtualDisk):
            data[x] = serialize_spec(xo)
        elif isinstance(xo, vim.vm.device.VirtualDeviceSpec.FileOperation):
            data[x] = serialize_spec(xo)
        elif isinstance(xo, vim.Description):
            data[x] = {
                'dynamicProperty': serialize_spec(xo.dynamicProperty),
                'dynamicType': serialize_spec(xo.dynamicType),
                'label': serialize_spec(xo.label),
                'summary': serialize_spec(xo.summary),
            }
        elif hasattr(xo, 'name'):
            data[x] = ((to_text(xo) + ':') + to_text(xo.name))
        elif isinstance(xo, vim.vm.ProfileSpec):
            pass
        elif issubclass(xt, list):
            data[x] = []
            for xe in xo:
                data[x].append(serialize_spec(xe))
        elif issubclass(xt, ((string_types + integer_types) + (float, bool))):
            data[x] = to_text(xt)
        elif issubclass(xt, bool):
            data[x] = xo
        elif issubclass(xt, dict):
            data[to_text(x)] = {
                
            }
            for (k, v) in xo.items():
                k = to_text(k)
                data[x][k] = serialize_spec(v)
        else:
            data[x] = str(xt)
    return data