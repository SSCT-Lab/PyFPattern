def _check_argument_types(self):
    ' ensure all arguments have the requested type '
    for (k, v) in self.argument_spec.items():
        wanted = v.get('type', None)
        if (k not in self.params):
            continue
        if (wanted is None):
            if (self.params[k] is None):
                continue
            wanted = 'str'
        value = self.params[k]
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