def search_by_name(service, name, **kwargs):
    "\n    Search for the entity by its name. Nested entities don't support search\n    via REST, so in case using search for nested entity we return all entities\n    and filter them by name.\n\n    :param service: service of the entity\n    :param name: name of the entity\n    :return: Entity object returned by Python SDK\n    "
    if ('search' in inspect.getargspec(service.list)[0]):
        res = service.list(search='name={name}'.format(name=name))
    else:
        res = [e for e in service.list() if (e.name == name)]
    if kwargs:
        res = [e for e in service.list() if (len([k for (k, v) in kwargs.items() if (getattr(e, k, None) == v)]) == len(kwargs))]
    res = (res or [None])
    return res[0]