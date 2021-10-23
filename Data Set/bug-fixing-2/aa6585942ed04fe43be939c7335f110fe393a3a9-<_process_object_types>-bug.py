

def _process_object_types(self, vobj, thisvm=None, inkey=None, level=0):
    ' Serialize an object '
    rdata = {
        
    }
    if ((type(vobj).__name__ in self.vimTableMaxDepth) and (level >= self.vimTableMaxDepth[type(vobj).__name__])):
        return rdata
    if (vobj is None):
        rdata = None
    elif (type(vobj) in self.vimTable):
        rdata = {
            
        }
        for key in self.vimTable[type(vobj)]:
            rdata[key] = getattr(vobj, key)
    elif (issubclass(type(vobj), str) or isinstance(vobj, str)):
        if vobj.isalnum():
            rdata = vobj
        else:
            rdata = vobj.decode('ascii', 'ignore')
    elif (issubclass(type(vobj), bool) or isinstance(vobj, bool)):
        rdata = vobj
    elif (issubclass(type(vobj), int) or isinstance(vobj, int)):
        rdata = vobj
    elif (issubclass(type(vobj), float) or isinstance(vobj, float)):
        rdata = vobj
    elif (issubclass(type(vobj), long) or isinstance(vobj, long)):
        rdata = vobj
    elif (issubclass(type(vobj), list) or issubclass(type(vobj), tuple)):
        rdata = []
        try:
            vobj = sorted(vobj)
        except Exception:
            pass
        for (idv, vii) in enumerate(vobj):
            if ((level + 1) <= self.maxlevel):
                vid = self._process_object_types(vii, thisvm=thisvm, inkey=(((inkey + '[') + str(idv)) + ']'), level=(level + 1))
                if vid:
                    rdata.append(vid)
    elif issubclass(type(vobj), dict):
        pass
    elif issubclass(type(vobj), object):
        methods = dir(vobj)
        methods = [str(x) for x in methods if (not x.startswith('_'))]
        methods = [x for x in methods if (x not in self.bad_types)]
        methods = [x for x in methods if (not (((inkey + '.') + x.lower()) in self.skip_keys))]
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
            if ((level + 1) <= self.maxlevel):
                try:
                    rdata[method] = self._process_object_types(methodToCall, thisvm=thisvm, inkey=((inkey + '.') + method), level=(level + 1))
                except vim.fault.NoPermission:
                    self.debugl(('Skipping method %s (NoPermission)' % method))
    else:
        pass
    return rdata
