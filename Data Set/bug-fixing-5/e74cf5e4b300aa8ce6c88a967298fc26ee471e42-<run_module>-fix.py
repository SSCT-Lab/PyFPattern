def run_module():
    module_args = dict(apply=dict(type='bool'), revert=dict(type='str', choices=['all', 'one']))
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True, required_one_of=[['apply', 'revert']])
    result = syspatch_run(module)
    module.exit_json(**result)