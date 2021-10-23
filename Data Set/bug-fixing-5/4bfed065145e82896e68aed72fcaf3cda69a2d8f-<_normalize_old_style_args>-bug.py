def _normalize_old_style_args(self, thing, action):
    "\n        deals with fuzziness in old-style (action/local_action) module invocations\n        returns tuple of (module_name, dictionary_args)\n\n        possible example inputs:\n            { 'local_action' : 'shell echo hi' }\n            { 'action'       : 'shell echo hi' }\n            { 'local_action' : { 'module' : 'ec2', 'x' : 1, 'y': 2 }}\n        standardized outputs like:\n            ( 'command', { _raw_params: 'echo hi', _uses_shell: True }\n        "
    if isinstance(thing, dict):
        args = thing
    elif isinstance(thing, string_types):
        check_raw = (action in ('command', 'net_command', 'win_command', 'shell', 'win_shell', 'script', 'raw'))
        args = parse_kv(thing, check_raw=check_raw)
    elif (thing is None):
        args = None
    else:
        raise AnsibleParserError(('unexpected parameter type in action: %s' % type(thing)), obj=self._task_ds)
    return args