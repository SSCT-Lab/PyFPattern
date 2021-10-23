def _api_params_from_map(self):
    result = dict()
    pmap = self.__class__.api_param_map
    for (k, v) in iteritems(pmap):
        value = getattr(self, k)
        result[v] = value
    return result