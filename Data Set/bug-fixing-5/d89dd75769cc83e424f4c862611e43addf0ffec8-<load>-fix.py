@staticmethod
def load(data, block=None, role=None, task_include=None, variable_manager=None, loader=None):
    ir = IncludeRole(block, role, task_include=task_include).load_data(data, variable_manager=variable_manager, loader=loader)
    my_arg_names = frozenset(ir.args.keys())
    ir._role_name = ir.args.get('name', ir.args.get('role'))
    if (ir._role_name is None):
        raise AnsibleParserError("'name' is a required field for include_role.")
    bad_opts = my_arg_names.difference(IncludeRole.VALID_ARGS)
    if bad_opts:
        raise AnsibleParserError(('Invalid options for include_role: %s' % ','.join(list(bad_opts))))
    for key in IncludeRole.FROM_ARGS.intersection(my_arg_names):
        from_key = key.replace('_from', '')
        ir._from_files[from_key] = basename(ir.args.get(key))
    for option in IncludeRole.OTHER_ARGS.intersection(my_arg_names):
        setattr(ir, option, ir.args.get(option))
    return ir