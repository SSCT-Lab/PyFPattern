@classmethod
def from_api(cls, params):
    for (key, value) in iteritems(cls.param_api_map):
        params[key] = params.pop(value, None)
    p = cls(params)
    return p