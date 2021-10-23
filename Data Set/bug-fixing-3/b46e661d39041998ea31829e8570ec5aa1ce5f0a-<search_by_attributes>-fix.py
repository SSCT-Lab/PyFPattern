def search_by_attributes(service, list_params=None, **kwargs):
    "\n    Search for the entity by attributes. Nested entities don't support search\n    via REST, so in case using search for nested entity we return all entities\n    and filter them by specified attributes.\n    "
    list_params = (list_params or {
        
    })
    if ('search' in inspect.getargspec(service.list)[0]):
        res = service.list(search=' and '.join(('{0}="{1}"'.format(k, v) for (k, v) in kwargs.items())), **list_params)
    else:
        res = [e for e in service.list(**list_params) if (len([k for (k, v) in kwargs.items() if (getattr(e, k, None) == v)]) == len(kwargs))]
    res = (res or [None])
    return res[0]