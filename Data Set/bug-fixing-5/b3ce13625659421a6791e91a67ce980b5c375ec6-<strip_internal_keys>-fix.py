def strip_internal_keys(dirty, exceptions=None):
    "\n    All keys starting with _ansible_ are internal, so create a copy of the 'dirty' dict\n    and remove them from the clean one before returning it\n    "
    if (exceptions is None):
        exceptions = ()
    clean = dirty.copy()
    for k in dirty.keys():
        if (isinstance(k, string_types) and k.startswith('_ansible_')):
            if (k not in exceptions):
                del clean[k]
        elif isinstance(dirty[k], dict):
            clean[k] = strip_internal_keys(dirty[k])
    return clean