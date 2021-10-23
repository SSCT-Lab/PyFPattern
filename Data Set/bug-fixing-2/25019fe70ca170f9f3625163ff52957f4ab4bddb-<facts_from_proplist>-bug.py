

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
                if (not val):
                    val = getattr(vm, x)
                else:
                    try:
                        val = getattr(val, x)
                    except AttributeError as e:
                        self.debugl(e)
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
