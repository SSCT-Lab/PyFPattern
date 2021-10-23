def main():
    argument_spec = dict(pkg=dict(required=True), file_system=dict(required=False, default='bootflash:'), include_defaults=dict(default=False), config=dict(), save=dict(type='bool', default=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    pkg = module.params['pkg']
    file_system = module.params['file_system']
    changed = False
    remote_exists = remote_file_exists(module, pkg, file_system=file_system)
    if (not remote_exists):
        module.fail_json(msg="The requested package doesn't exist on the device")
    commands = get_commands(module, pkg, file_system)
    if ((not module.check_mode) and commands):
        apply_patch(module, commands)
        changed = True
    if ('configure' in commands):
        commands.pop(0)
    module.exit_json(changed=changed, pkg=pkg, file_system=file_system, updates=commands)