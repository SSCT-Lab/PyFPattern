def main():
    argument_spec = dict(system_image_file=dict(required=True), kickstart_image_file=dict(required=False), issu=dict(choices=['required', 'desired', 'no', 'yes'], default='no'))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    check_ansible_timer(module)
    sif = module.params['system_image_file']
    kif = module.params['kickstart_image_file']
    issu = module.params['issu']
    if ((kif == 'null') or (kif == '')):
        kif = None
    install_result = do_install_all(module, issu, sif, kick=kif)
    if install_result['error']:
        msg = 'Failed to upgrade device using image '
        if kif:
            msg = (msg + ('files: kickstart: %s, system: %s' % (kif, sif)))
        else:
            msg = (msg + ('file: system: %s' % sif))
        module.fail_json(msg=msg, raw_data=install_result['list_data'])
    state = install_result['processed']
    changed = install_result['upgrade_needed']
    module.exit_json(changed=changed, install_state=state, warnings=warnings)