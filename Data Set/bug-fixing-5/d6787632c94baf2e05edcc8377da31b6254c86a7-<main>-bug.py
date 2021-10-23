def main():
    'main entry point for module execution\n    '
    argument_spec = dict(commands=dict(type='list', required=True), wait_for=dict(type='list', aliases=['waitfor']), match=dict(default='all', choices=['all', 'any']), retries=dict(default=10, type='int'), interval=dict(default=1, type='int'))
    argument_spec.update(ios_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    result = {
        'changed': False,
    }
    warnings = list()
    check_args(module, warnings)
    commands = parse_commands(module, warnings)
    result['warnings'] = warnings
    wait_for = (module.params['wait_for'] or list())
    conditionals = [Conditional(c) for c in wait_for]
    retries = module.params['retries']
    interval = module.params['interval']
    match = module.params['match']
    while (retries > 0):
        responses = run_commands(module, commands)
        for item in list(conditionals):
            if item(responses):
                if (match == 'any'):
                    conditionals = list()
                    break
                conditionals.remove(item)
        if (not conditionals):
            break
        time.sleep(interval)
        retries -= 1
    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = 'One or more conditional statements have not be satisfied'
        module.fail_json(msg=msg, failed_conditions=failed_conditions)
    result = {
        'changed': False,
        'stdout': responses,
        'stdout_lines': list(to_lines(responses)),
    }
    module.exit_json(**result)