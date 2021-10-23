def main():
    argument_spec = dict(pkg=dict(required=True), file_system=dict(required=False, default='bootflash:'))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    results = {
        'changed': False,
        'commands': [],
        'warnings': warnings,
    }
    pkg = module.params['pkg']
    file_system = module.params['file_system']
    remote_exists = remote_file_exists(module, pkg, file_system=file_system)
    if (not remote_exists):
        module.fail_json(msg="The requested package doesn't exist on the device")
    commands = get_commands(module, pkg, file_system)
    if commands:
        results['changed'] = True
        if (not module.check_mode):
            apply_patch(module, commands)
        if ('configure' in commands):
            commands.pop(0)
        results['commands'] = commands
    module.exit_json(**results)