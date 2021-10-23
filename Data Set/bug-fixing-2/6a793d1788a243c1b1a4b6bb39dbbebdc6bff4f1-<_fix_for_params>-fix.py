

def _fix_for_params(self, query, params, unify_by_values=False):
    if (query.endswith(';') or query.endswith('/')):
        query = query[:(- 1)]
    if (params is None):
        params = []
    elif hasattr(params, 'keys'):
        args = {k: (':%s' % k) for k in params}
        query = (query % args)
    elif (unify_by_values and (len(params) > 0)):
        params_dict = {param: (':arg%d' % i) for (i, param) in enumerate(set(params))}
        args = [params_dict[param] for param in params]
        params = {value: key for (key, value) in params_dict.items()}
        query = (query % tuple(args))
    else:
        args = [(':arg%d' % i) for i in range(len(params))]
        query = (query % tuple(args))
    return (query, self._format_params(params))
