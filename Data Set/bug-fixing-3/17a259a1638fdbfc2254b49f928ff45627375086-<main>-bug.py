def main():
    argument_spec = dict(local_file=dict(required=True), remote_file=dict(required=False), file_system=dict(required=False, default='bootflash:'), include_defaults=dict(default=True), config=dict(), save=dict(type='bool', default=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_SCP):
        module.fail_json(msg='library scp is required but does not appear to be installed. It can be installed using `pip install scp`')
    warnings = list()
    check_args(module, warnings)
    results = dict(changed=False, warnings=warnings)
    local_file = module.params['local_file']
    remote_file = module.params['remote_file']
    file_system = module.params['file_system']
    results['transfer_status'] = 'No Transfer'
    results['local_file'] = local_file
    results['file_system'] = file_system
    if (not local_file_exists(module)):
        module.fail_json(msg='Local file {} not found'.format(local_file))
    dest = (remote_file or os.path.basename(local_file))
    remote_exists = remote_file_exists(module, dest, file_system=file_system)
    if (not remote_exists):
        results['changed'] = True
        file_exists = False
    else:
        file_exists = True
    if ((not module.check_mode) and (not file_exists)):
        transfer_file(module, dest)
        results['transfer_status'] = 'Sent'
    if (remote_file is None):
        remote_file = os.path.basename(local_file)
    results['remote_file'] = remote_file
    module.exit_json(**results)