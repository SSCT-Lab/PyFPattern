def _check_argument_types(self, spec=None, param=None):
    ' ensure all arguments have the requested type '
    if (spec is None):
        spec = self.argument_spec
    if (param is None):
        param = self.params
    for (k, v) in spec.items():
        wanted = v.get('type', None)
        if (k not in param):
            continue
        if (wanted is None):
            if (self.params[k] is None):
                continue
            wanted = 'str'
        value = param[k]
        if (value is None):
            continue
        try:
            type_checker = self._CHECK_ARGUMENT_TYPES_DISPATCHER[wanted]
        except KeyError:
            self.fail_json(msg=('implementation error: unknown type %s requested for %s' % (wanted, k)))
        try:
            self.params[k] = type_checker(value)
        except (TypeError, ValueError):
            e = get_exception()
            self.fail_json(msg=('argument %s is of type %s and we were unable to convert to %s: %s' % (k, type(value), wanted, e)))
        spec = None
        if ((wanted == 'dict') or ((wanted == 'list') and (v.get('elements', '') == 'dict'))):
            spec = v.get('options', None)
            if spec:
                self._check_required_arguments(spec, param[k])
                self._check_argument_types(spec, param[k])
                self._check_argument_values(spec, param[k])