def validate_query_parameters(self, x):
    if (not (isinstance(x, dict) and (len(x) == 1))):
        self.display.warning(('Warning query parameters %s not a dict with a single key.' % x))
        return
    k = tuple(x.keys())[0]
    v = tuple(x.values())[0]
    if (not ((k in ALLOWED_DEVICE_QUERY_PARAMETERS) or k.startswith('cf_'))):
        self.display.warning(('Warning: %s not in %s or starting with cf (Custom field)' % (k, ALLOWED_DEVICE_QUERY_PARAMETERS)))
        return
    return (k, v)