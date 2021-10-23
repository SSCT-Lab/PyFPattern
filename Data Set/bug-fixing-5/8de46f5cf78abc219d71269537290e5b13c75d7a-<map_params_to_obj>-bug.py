def map_params_to_obj(module):
    aggregate = module.params['aggregate']
    if (not aggregate):
        if ((not module.params['name']) and module.params['purge']):
            return list()
        elif (not module.params['name']):
            module.fail_json(msg='missing required argument: name')
        else:
            collection = [{
                'name': module.params['name'],
            }]
    else:
        collection = list()
        for item in aggregate:
            if (not isinstance(item, dict)):
                collection.append({
                    'username': item,
                })
            elif ('name' not in item):
                module.fail_json(msg='missing required argument: name')
            else:
                collection.append(item)
    objects = list()
    for item in collection:
        get_value = partial(get_param_value, item=item, module=module)
        item.update({
            'full_name': get_value('full_name'),
            'role': get_value('role'),
            'sshkey': get_value('sshkey'),
            'state': get_value('state'),
            'active': get_value('active'),
        })
        for (key, value) in iteritems(item):
            validator = globals().get(('validate_%s' % key))
            if all((value, validator)):
                validator(value, module)
        objects.append(item)
    return objects