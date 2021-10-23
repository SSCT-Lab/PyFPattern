def _normalize_parameters(self, thing, action=None, additional_args=dict()):
    '\n        arguments can be fuzzy.  Deal with all the forms.\n        '
    final_args = dict()
    if additional_args:
        if isinstance(additional_args, string_types):
            templar = Templar(loader=None)
            if templar._contains_vars(additional_args):
                final_args['_variable_params'] = additional_args
            else:
                raise AnsibleParserError("Complex args containing variables cannot use bare variables, and must use the full variable style ('{{var_name}}')")
        elif isinstance(additional_args, dict):
            final_args.update(additional_args)
        else:
            raise AnsibleParserError('Complex args must be a dictionary or variable string ("{{var}}").')
    if (action is not None):
        args = self._normalize_new_style_args(thing, action)
    else:
        (action, args) = self._normalize_old_style_args(thing)
        if (args and ('args' in args)):
            tmp_args = args.pop('args')
            if isinstance(tmp_args, string_types):
                tmp_args = parse_kv(tmp_args)
            args.update(tmp_args)
    if (args and (action not in ('command', 'net_command', 'win_command', 'shell', 'win_shell', 'script', 'raw'))):
        for arg in args:
            arg = to_text(arg)
            if arg.startswith('_ansible_'):
                raise AnsibleError(("invalid parameter specified for action '%s': '%s'" % (action, arg)))
    if args:
        final_args.update(args)
    return (action, final_args)