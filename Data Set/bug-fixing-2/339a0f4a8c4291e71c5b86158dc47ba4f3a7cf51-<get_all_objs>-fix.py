

def get_all_objs(self, content, types, confine_to_datacenter=True):
    ' Wrapper around get_all_objs to set datacenter context '
    objects = get_all_objs(content, types)
    if confine_to_datacenter:
        if hasattr(objects, 'items'):
            tmpobjs = objects.copy()
            for (k, v) in objects.items():
                parent_dc = get_parent_datacenter(k)
                if (parent_dc.name != self.dc_name):
                    tmpobjs.pop(k, None)
            objects = tmpobjs
        else:
            objects = [x for x in objects if (get_parent_datacenter(x).name == self.dc_name)]
    return objects
