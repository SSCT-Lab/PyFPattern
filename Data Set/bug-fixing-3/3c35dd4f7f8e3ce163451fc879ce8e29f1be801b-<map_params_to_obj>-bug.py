def map_params_to_obj(module):
    obj = []
    aggregate = module.params.get('aggregate')
    if aggregate:
        for item in aggregate:
            for key in item:
                if (item.get(key) is None):
                    item[key] = module.params[key]
            d = item.copy()
            d['group'] = str(d['group'])
            d['min_links'] = str(d['min_links'])
            obj.append(d)
    else:
        obj.append({
            'group': str(module.params['group']),
            'mode': module.params['mode'],
            'min_links': str(module.params['min_links']),
            'members': module.params['members'],
            'state': module.params['state'],
        })
    return obj