def _normalize_old_style_args(self, thing):
    "\n        deals with fuzziness in old-style (action/local_action) module invocations\n        returns tuple of (module_name, dictionary_args)\n\n        possible example inputs:\n           { 'shell' : 'echo hi' }\n           'shell echo hi'\n           {'module': 'ec2', 'x': 1 }\n        standardized outputs like:\n           ('ec2', { 'x': 1} )\n        "
    action = None
    args = None
    actions_allowing_raw = ('command', 'win_command', 'shell', 'win_shell', 'script', 'raw')
    if isinstance(thing, dict):
        thing = thing.copy()
        if ('module' in thing):
            (action, module_args) = self._split_module_string(thing['module'])
            args = thing.copy()
            check_raw = (action in actions_allowing_raw)
            args.update(parse_kv(module_args, check_raw=check_raw))
            del args['module']
    elif isinstance(thing, string_types):
        (action, args) = self._split_module_string(thing)
        check_raw = (action in actions_allowing_raw)
        args = parse_kv(args, check_raw=check_raw)
    else:
        raise AnsibleParserError(('unexpected parameter type in action: %s' % type(thing)), obj=self._task_ds)
    return (action, args)