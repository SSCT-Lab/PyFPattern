def _check_argument_values(self):
    ' ensure all arguments have the requested values, and there are no stray arguments '
    for (k, v) in self.argument_spec.items():
        choices = v.get('choices', None)
        if (choices is None):
            continue
        if isinstance(choices, SEQUENCETYPE):
            if (k in self.params):
                if (self.params[k] not in choices):
                    lowered_choices = None
                    if (self.params[k] == 'False'):
                        lowered_choices = _lenient_lowercase(choices)
                        FALSEY = frozenset(BOOLEANS_FALSE)
                        overlap = FALSEY.intersection(choices)
                        if (len(overlap) == 1):
                            (self.params[k],) = overlap
                    if (self.params[k] == 'True'):
                        if (lowered_choices is None):
                            lowered_choices = _lenient_lowercase(choices)
                        TRUTHY = frozenset(BOOLEANS_TRUE)
                        overlap = TRUTHY.intersection(choices)
                        if (len(overlap) == 1):
                            (self.params[k],) = overlap
                    if (self.params[k] not in choices):
                        choices_str = ','.join([str(c) for c in choices])
                        msg = ('value of %s must be one of: %s, got: %s' % (k, choices_str, self.params[k]))
                        self.fail_json(msg=msg)
        else:
            self.fail_json(msg=('internal error: choices for argument %s are not iterable: %s' % (k, choices)))