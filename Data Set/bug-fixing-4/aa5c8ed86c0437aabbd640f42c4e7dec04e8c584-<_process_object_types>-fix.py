def _process_object_types(self, vobj, level=0):
    rdata = {
        
    }
    self.debugl(('PROCESSING: %s' % str(vobj)))
    if (type(vobj) in self.safe_types):
        try:
            rdata = vobj
        except Exception as e:
            self.debugl(str(e))
    elif hasattr(vobj, 'append'):
        rdata = []
        for vi in sorted(vobj):
            if (type(vi) in self.safe_types):
                rdata.append(vi)
            elif ((level + 1) <= self.maxlevel):
                vid = self.facts_from_vobj(vi, level=(level + 1))
                if vid:
                    rdata.append(vid)
    elif hasattr(vobj, '__dict__'):
        if ((level + 1) <= self.maxlevel):
            md = None
            md = self.facts_from_vobj(vobj, level=(level + 1))
            if md:
                rdata = md
    elif ((not vobj) or (type(vobj) in self.safe_types)):
        rdata = vobj
    elif (type(vobj) == datetime.datetime):
        rdata = str(vobj)
    else:
        self.debugl(('unknown datatype: %s' % type(vobj)))
    if (not rdata):
        rdata = None
    return rdata