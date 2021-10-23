def get_object_ref(self, ib_obj_type, obj_filter, ib_spec):
    ' this function gets and returns the current object based on name/old_name passed'
    update = False
    old_name = new_name = None
    try:
        name_obj = self.module._check_type_dict(obj_filter['name'])
        old_name = name_obj['old_name']
        new_name = name_obj['new_name']
    except TypeError:
        name = obj_filter['name']
    if (old_name and new_name):
        if (ib_obj_type == NIOS_HOST_RECORD):
            test_obj_filter = dict([('name', old_name), ('view', obj_filter['view'])])
        else:
            test_obj_filter = dict([('name', old_name)])
        ib_obj = self.get_object(ib_obj_type, test_obj_filter, return_fields=ib_spec.keys())
        if ib_obj:
            obj_filter['name'] = new_name
        else:
            test_obj_filter['name'] = new_name
            ib_obj = self.get_object(ib_obj_type, test_obj_filter, return_fields=ib_spec.keys())
        update = True
        return (ib_obj, update, new_name)
    if (ib_obj_type == NIOS_HOST_RECORD):
        if (not obj_filter['configure_for_dns']):
            test_obj_filter = dict([('name', name)])
        else:
            test_obj_filter = dict([('name', name), ('view', obj_filter['view'])])
    else:
        test_obj_filter = dict([('name', name)])
    ib_obj = self.get_object(ib_obj_type, test_obj_filter.copy(), return_fields=ib_spec.keys())
    return (ib_obj, update, new_name)