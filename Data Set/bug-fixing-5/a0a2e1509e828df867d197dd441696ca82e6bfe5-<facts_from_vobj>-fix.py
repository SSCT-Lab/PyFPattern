def facts_from_vobj(self, vobj, level=0):
    ' Traverse a VM object and return a json compliant data structure '
    if (level == 0):
        try:
            self.debugl(('# get facts: %s' % vobj.name))
        except Exception as e:
            self.debugl(e)
    rdata = {
        
    }
    methods = dir(vobj)
    methods = [str(x) for x in methods if (not x.startswith('_'))]
    methods = [x for x in methods if (not (x in self.bad_types))]
    methods = sorted(methods)
    for method in methods:
        try:
            methodToCall = getattr(vobj, method)
        except Exception as e:
            continue
        if callable(methodToCall):
            continue
        if self.lowerkeys:
            method = method.lower()
        rdata[method] = self._process_object_types(methodToCall)
    return rdata