def _process_object_types(self, vobj, level=0):
    ' Serialize an object '
    rdata = {
        
    }
    if (vobj is None):
        rdata = None
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
        except Exception as e:
            pass
        for vi in vobj:
            if ((level + 1) <= self.maxlevel):
                vid = self._process_object_types(vi, level=(level + 1))
                if vid:
                    rdata.append(vid)
    elif issubclass(type(vobj), dict):
        pass
    elif issubclass(type(vobj), object):
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
            if ((level + 1) <= self.maxlevel):
                rdata[method] = self._process_object_types(methodToCall, level=(level + 1))
    else:
        pass
    if (not rdata):
        rdata = None
    return rdata