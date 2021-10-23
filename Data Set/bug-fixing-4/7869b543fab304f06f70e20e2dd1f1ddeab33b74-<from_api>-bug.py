@classmethod
def from_api(cls, params):
    for (key, value) in iteritems(cls._api_param_map):
        params[key] = params.pop(value, None)
    p = cls(params)
    return p