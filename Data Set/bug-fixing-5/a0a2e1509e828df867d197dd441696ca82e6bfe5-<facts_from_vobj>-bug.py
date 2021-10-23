def facts_from_vobj(self, vobj, level=0):
    ' Traverse a VM object and return a json compliant data structure '
    rdata = {
        
    }
    if hasattr(vobj, '__name__'):
        if (vobj.__name__ == 'VMWareInventory'):
            return rdata
    if (level > self.maxlevel):
        return rdata
    if (hasattr(vobj, '__dict__') and (not (level == 0))):
        keys = sorted(vobj.__dict__.keys())
        for k in keys:
            v = vobj.__dict__[k]
            if k.startswith('_'):
                continue
            if (k.lower() in self.skip_keys):
                continue
            if self.lowerkeys:
                k = k.lower()
            rdata[k] = self._process_object_types(v, level=level)
    else:
        methods = dir(vobj)
        methods = [str(x) for x in methods if (not x.startswith('_'))]
        methods = [x for x in methods if (not (x in self.bad_types))]
        methods = sorted(methods)
        for method in methods:
            if (method in rdata):
                continue
            try:
                methodToCall = getattr(vobj, method)
            except Exception as e:
                continue
            if callable(methodToCall):
                continue
            if self.lowerkeys:
                method = method.lower()
            rdata[method] = self._process_object_types(methodToCall, level=level)
    return rdata