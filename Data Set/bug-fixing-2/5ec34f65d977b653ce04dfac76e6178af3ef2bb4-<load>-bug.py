

@staticmethod
def load(data, block=None, role=None, task_include=None, variable_manager=None, loader=None):
    ir = IncludeRole(block, role, task_include=task_include).load_data(data, variable_manager=variable_manager, loader=loader)
    my_arg_names = frozenset(ir.args.keys())
    ir._role_name = ir.args.get('name', ir.args.get('role'))
    if (ir._role_name is None):
        raise AnsibleParserError(("'name' is a required field for %s." % ir.action))
    bad_opts = my_arg_names.difference(IncludeRole.VALID_ARGS)
    if bad_opts:
        raise AnsibleParserError(('Invalid options for %s: %s' % (ir.action, ','.join(list(bad_opts)))))
    for key in my_arg_names.intersection(IncludeRole.FROM_ARGS):
        from_key = key.replace('_from', '')
        ir._from_files[from_key] = basename(ir.args.get(key))
    for option in my_arg_names.intersection(IncludeRole.OTHER_ARGS):
        setattr(ir, option, ir.args.get(option))
    return ir
