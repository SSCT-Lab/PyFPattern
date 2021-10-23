@staticmethod
def load(data, block=None, role=None, task_include=None, variable_manager=None, loader=None):
    ir = IncludeRole(block, role, task_include=task_include).load_data(data, variable_manager=variable_manager, loader=loader)
    ir._role_name = ir.args.get('name', ir.args.get('role'))
    if (ir._role_name is None):
        raise AnsibleParserError("'name' is a required field for include_role.")
    for key in ['tasks', 'vars', 'defaults']:
        from_key = ('%s_from' % key)
        if ir.args.get(from_key):
            ir._from_files[key] = basename(ir.args.get(from_key))
    for option in ['private', 'allow_duplicates']:
        if (option in ir.args):
            setattr(ir, option, ir.args.get(option))
    return ir