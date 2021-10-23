def validate_query_parameters(self, x):
    if (not (isinstance(x, dict) and (len(x) == 1))):
        self.display.warning(('Warning query parameters %s not a dict with a single key.' % x))
        return
    k = tuple(x.keys())[0]
    v = tuple(x.values())[0]
    if (not ((k in ALLOWED_DEVICE_QUERY_PARAMETERS) or k.startswith('cf_'))):
        msg = ('Warning: %s not in %s or starting with cf (Custom field)' % (k, ALLOWED_DEVICE_QUERY_PARAMETERS))
        self.display.warning(msg=msg)
        return
    return (k, v)