def main():
    ' Main entry point for Ansible module execution\n    '
    argument_spec = dict(src=dict(type='path', required=True, aliases=['package']), version=dict(), reboot=dict(type='bool', default=True), no_copy=dict(default=False, type='bool'), force=dict(type='bool', default=False), transport=dict(default='netconf', choices=['netconf']))
    argument_spec.update(junos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (module.params['provider'] is None):
        module.params['provider'] = {
            
        }
    if (not HAS_PYEZ):
        module.fail_json(msg='junos-eznc is required but does not appear to be installed. It can be installed using `pip  install junos-eznc`')
    result = dict(changed=False)
    do_upgrade = (module.params['force'] or False)
    device = connect(module)
    if (not module.params['force']):
        facts = device.facts_refresh()
        has_ver = device.facts.get('version')
        wants_ver = module.params['version']
        do_upgrade = (has_ver != wants_ver)
    if do_upgrade:
        if (not module.check_mode):
            install_package(module, device)
        result['changed'] = True
    module.exit_json(**result)