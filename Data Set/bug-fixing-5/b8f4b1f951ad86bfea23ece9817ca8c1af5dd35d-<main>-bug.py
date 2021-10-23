def main():
    spec = dict(commands=dict(type='list', required=True), wait_for=dict(type='list', aliases=['waitfor']), match=dict(default='all', choices=['all', 'any']), retries=dict(default=10, type='int'), interval=dict(default=1, type='int'))
    spec.update(vyos_argument_spec)
    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    commands = parse_commands(module, warnings)
    wait_for = (module.params['wait_for'] or list())
    conditionals = [Conditional(c) for c in wait_for]
    retries = module.params['retries']
    interval = module.params['interval']
    match = module.params['match']
    for _ in range(retries):
        responses = run_commands(module, commands)
        for item in conditionals:
            if item(responses):
                if (match == 'any'):
                    conditionals = list()
                    break
                conditionals.remove(item)
            if (not conditionals):
                break
            time.sleep(interval)
    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = 'One or more conditional statements have not been satisfied'
        module.fail_json(msg=msg, falied_conditions=failed_conditions)
    result = {
        'changed': False,
        'stdout': responses,
        'warnings': warnings,
        'stdout_lines': list(to_lines(responses)),
    }
    module.exit_json(**result)