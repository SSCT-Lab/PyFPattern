def main():
    spec = dict(src=dict(type='path', required=True, aliases=['package']), version=dict(), reboot=dict(type='bool', default=True), no_copy=dict(default=False, type='bool'), force=dict(type='bool', default=False), transport=dict(default='netconf', choices=['netconf']))
    module = NetworkModule(argument_spec=spec, supports_check_mode=True)
    if (not HAS_SW):
        module.fail_json(msg='Missing jnpr.junos.utils.sw module')
    result = dict(changed=False)
    do_upgrade = (module.params['force'] or False)
    if (not module.params['force']):
        has_ver = module.connection.get_facts().get('version')
        wants_ver = module.params['version']
        do_upgrade = (has_ver != wants_ver)
    if do_upgrade:
        if (not module.check_mode):
            install_package(module)
        result['changed'] = True
    module.exit_json(**result)