def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True, aliases=['pkg'], type='list'), state=dict(required=False, default='present', choices=['absent', 'installed', 'latest', 'present', 'removed', 'dist-upgrade']), type=dict(required=False, default='package', choices=['package', 'patch', 'pattern', 'product', 'srcpackage', 'application']), extra_args_precommand=dict(required=False, default=None), disable_gpg_check=dict(required=False, default='no', type='bool'), disable_recommends=dict(required=False, default='yes', type='bool'), force=dict(required=False, default='no', type='bool'), update_cache=dict(required=False, aliases=['refresh'], default='no', type='bool'), oldpackage=dict(required=False, default='no', type='bool'), extra_args=dict(required=False, default=None)), supports_check_mode=True)
    name = module.params['name']
    state = module.params['state']
    update_cache = module.params['update_cache']
    name = list(filter(None, name))
    if (update_cache and (not module.check_mode)):
        retvals = repo_refresh(module)
        if (retvals['rc'] != 0):
            module.fail_json(msg='Zypper refresh run failed.', **retvals)
    if ((name == ['*']) and (state in ['latest', 'dist-upgrade'])):
        (packages_changed, retvals) = package_update_all(module)
    elif ((name != ['*']) and (state == 'dist-upgrade')):
        module.fail_json(msg='Can not dist-upgrade specific packages.')
    elif (state in ['absent', 'removed']):
        (packages_changed, retvals) = package_absent(module, name)
    elif (state in ['installed', 'present', 'latest']):
        (packages_changed, retvals) = package_present(module, name, (state == 'latest'))
    retvals['changed'] = ((retvals['rc'] == 0) and bool(packages_changed))
    if module._diff:
        set_diff(module, retvals, packages_changed)
    if (retvals['rc'] != 0):
        module.fail_json(msg='Zypper run failed.', **retvals)
    if (not retvals['changed']):
        del retvals['stdout']
        del retvals['stderr']
    module.exit_json(name=name, state=state, update_cache=update_cache, **retvals)