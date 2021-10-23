def run(self, ib_obj_type, ib_spec):
    ' Runs the module and performans configuration tasks\n        :args ib_obj_type: the WAPI object type to operate against\n        :args ib_spec: the specification for the WAPI object as a dict\n        :returns: a results dict\n        '
    update = new_name = None
    state = self.module.params['state']
    if (state not in ('present', 'absent')):
        self.module.fail_json(msg=('state must be one of `present`, `absent`, got `%s`' % state))
    result = {
        'changed': False,
    }
    obj_filter = dict([(k, self.module.params[k]) for (k, v) in iteritems(ib_spec) if v.get('ib_req')])
    (ib_obj_ref, update, new_name) = self.get_object_ref(self.module, ib_obj_type, obj_filter, ib_spec)
    if ib_obj_ref:
        current_object = ib_obj_ref[0]
        if ('extattrs' in current_object):
            current_object['extattrs'] = flatten_extattrs(current_object['extattrs'])
        ref = current_object.pop('_ref')
    else:
        current_object = obj_filter
        ref = None
    proposed_object = {
        
    }
    for (key, value) in iteritems(ib_spec):
        if (self.module.params[key] is not None):
            if ('transform' in value):
                proposed_object[key] = value['transform'](self.module)
            else:
                proposed_object[key] = self.module.params[key]
    if (update and new_name):
        proposed_object['name'] = new_name
    res = None
    modified = (not self.compare_objects(current_object, proposed_object))
    if ('extattrs' in proposed_object):
        proposed_object['extattrs'] = normalize_extattrs(proposed_object['extattrs'])
    if (state == 'present'):
        if (ref is None):
            if (not self.module.check_mode):
                self.create_object(ib_obj_type, proposed_object)
            result['changed'] = True
        elif modified:
            self.check_if_recordname_exists(obj_filter, ib_obj_ref, ib_obj_type, current_object, proposed_object)
            if (ib_obj_type in (NIOS_HOST_RECORD, NIOS_NETWORK_VIEW, NIOS_DNS_VIEW)):
                proposed_object = self.on_update(proposed_object, ib_spec)
                res = self.update_object(ref, proposed_object)
            elif ('network_view' in proposed_object):
                proposed_object.pop('network_view')
            if ((not self.module.check_mode) and (res is None)):
                proposed_object = self.on_update(proposed_object, ib_spec)
                self.update_object(ref, proposed_object)
            result['changed'] = True
    elif (state == 'absent'):
        if (ref is not None):
            if (not self.module.check_mode):
                self.delete_object(ref)
            result['changed'] = True
    return result