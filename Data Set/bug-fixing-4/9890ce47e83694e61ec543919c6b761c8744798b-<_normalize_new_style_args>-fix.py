def _normalize_new_style_args(self, thing, action):
    "\n        deals with fuzziness in new style module invocations\n        accepting key=value pairs and dictionaries, and returns\n        a dictionary of arguments\n\n        possible example inputs:\n            'echo hi', 'shell'\n            {'region': 'xyz'}, 'ec2'\n        standardized outputs like:\n            { _raw_params: 'echo hi', _uses_shell: True }\n        "
    if isinstance(thing, dict):
        args = thing
    elif isinstance(thing, string_types):
        check_raw = (action in FREEFORM_ACTIONS)
        args = parse_kv(thing, check_raw=check_raw)
    elif (thing is None):
        args = None
    else:
        raise AnsibleParserError(('unexpected parameter type in action: %s' % type(thing)), obj=self._task_ds)
    return args