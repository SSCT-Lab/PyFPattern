def main():
    argument_spec = dict(system_image_file=dict(required=True), kickstart_image_file=dict(required=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    system_image_file = module.params['system_image_file']
    kickstart_image_file = module.params['kickstart_image_file']
    if (kickstart_image_file == 'null'):
        kickstart_image_file = None
    current_boot_options = get_boot_options(module)
    changed = False
    if (not already_set(current_boot_options, system_image_file, kickstart_image_file)):
        changed = True
    install_state = current_boot_options
    if ((not module.check_mode) and (changed is True)):
        set_boot_options(module, system_image_file, kickstart=kickstart_image_file)
        if (not already_set(install_state, system_image_file, kickstart_image_file)):
            module.fail_json(msg='Install not successful', install_state=install_state)
    module.exit_json(changed=changed, install_state=install_state, warnings=warnings)