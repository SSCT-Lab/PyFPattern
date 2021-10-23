def _check_argument_values(self):
    ' ensure all arguments have the requested values, and there are no stray arguments '
    for (k, v) in self.argument_spec.items():
        choices = v.get('choices', None)
        if (choices is None):
            continue
        if isinstance(choices, SEQUENCETYPE):
            if (k in self.params):
                if (self.params[k] not in choices):
                    choices_str = ','.join([str(c) for c in choices])
                    msg = ('value of %s must be one of: %s, got: %s' % (k, choices_str, self.params[k]))
                    self.fail_json(msg=msg)
        else:
            self.fail_json(msg=('internal error: choices for argument %s are not iterable: %s' % (k, choices)))