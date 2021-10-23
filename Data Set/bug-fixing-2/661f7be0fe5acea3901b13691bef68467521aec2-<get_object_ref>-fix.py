

def get_object_ref(self, module, ib_obj_type, obj_filter, ib_spec):
    ' this function gets the reference object of pre-existing nios objects '
    update = False
    old_name = new_name = None
    if ('name' in obj_filter):
        try:
            name_obj = self.module._check_type_dict(obj_filter['name'])
            old_name = name_obj['old_name']
            new_name = name_obj['new_name']
        except TypeError:
            name = obj_filter['name']
        if (old_name and new_name):
            if (ib_obj_type == NIOS_HOST_RECORD):
                test_obj_filter = dict([('name', old_name), ('view', obj_filter['view'])])
            elif (ib_obj_type in (NIOS_AAAA_RECORD, NIOS_A_RECORD)):
                test_obj_filter = obj_filter
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
        elif ((ib_obj_type == NIOS_IPV4_FIXED_ADDRESS) or ((ib_obj_type == NIOS_IPV6_FIXED_ADDRESS) and ('mac' in obj_filter))):
            test_obj_filter = dict([['mac', obj_filter['mac']]])
        elif (ib_obj_type == NIOS_A_RECORD):
            test_obj_filter = obj_filter
            test_obj_filter['name'] = test_obj_filter['name'].lower()
        else:
            test_obj_filter = obj_filter
        ib_obj = self.get_object(ib_obj_type, test_obj_filter.copy(), return_fields=ib_spec.keys())
    elif (ib_obj_type == NIOS_ZONE):
        temp = ib_spec['restart_if_needed']
        del ib_spec['restart_if_needed']
        ib_obj = self.get_object(ib_obj_type, obj_filter.copy(), return_fields=ib_spec.keys())
        if (not ib_obj):
            ib_spec['restart_if_needed'] = temp
    elif (ib_obj_type == NIOS_MEMBER):
        temp = ib_spec['create_token']
        del ib_spec['create_token']
        ib_obj = self.get_object(ib_obj_type, obj_filter.copy(), return_fields=ib_spec.keys())
        if temp:
            ib_spec['create_token'] = temp
    else:
        ib_obj = self.get_object(ib_obj_type, obj_filter.copy(), return_fields=ib_spec.keys())
    return (ib_obj, update, new_name)
