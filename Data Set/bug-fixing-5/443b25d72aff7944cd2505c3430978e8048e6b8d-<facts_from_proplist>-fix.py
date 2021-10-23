def facts_from_proplist(self, vm):
    'Get specific properties instead of serializing everything'
    rdata = {
        
    }
    for prop in self.guest_props:
        self.debugl(('getting %s property for %s' % (prop, vm.name)))
        key = prop
        if self.lowerkeys:
            key = key.lower()
        if ('.' not in prop):
            rdata[key] = getattr(vm, prop)
        else:
            parts = prop.split('.')
            total = (len(parts) - 1)
            val = None
            lastref = rdata
            for (idx, x) in enumerate(parts):
                if isinstance(val, dict):
                    if (x in val):
                        val = val.get(x)
                    elif (x.lower() in val):
                        val = val.get(x.lower())
                else:
                    if (not val):
                        try:
                            val = getattr(vm, x)
                        except AttributeError as e:
                            self.debugl(e)
                    else:
                        try:
                            val = getattr(val, x)
                        except AttributeError as e:
                            self.debugl(e)
                    val = self._process_object_types(val)
                if self.lowerkeys:
                    x = x.lower()
                if (idx != total):
                    if (x not in lastref):
                        lastref[x] = {
                            
                        }
                    lastref = lastref[x]
                else:
                    lastref[x] = val
    return rdata