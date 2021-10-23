def run(self, terms, variables=None, **kwargs):
    try:
        obj_type = terms[0]
    except IndexError:
        raise AnsibleError('the object_type must be specified')
    return_fields = kwargs.pop('return_fields', None)
    filter_data = kwargs.pop('filter', {
        
    })
    extattrs = normalize_extattrs(kwargs.pop('extattrs', {
        
    }))
    provider = kwargs.pop('provider', {
        
    })
    wapi = WapiLookup(provider)
    res = wapi.get_object(obj_type, filter_data, return_fields=return_fields)
    if (res is not None):
        for obj in res:
            if ('extattrs' in obj):
                obj['extattrs'] = flatten_extattrs(obj['extattrs'])
    else:
        res = []
    return res