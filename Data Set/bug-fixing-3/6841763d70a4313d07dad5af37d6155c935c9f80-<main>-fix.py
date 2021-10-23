def main():
    module = AnsibleModule(argument_spec=dict(state=dict(default='installed', choices=['installed', 'removed', 'absent', 'present']), update_cache=dict(default=False, aliases=['update-cache'], type='bool'), force=dict(default=True, type='bool'), no_recommends=dict(default=True, aliases=['no-recommends'], type='bool'), package=dict(aliases=['pkg', 'name'], required=True), root=dict(aliases=['installroot'])))
    if (not os.path.exists(URPMI_PATH)):
        module.fail_json(msg=('cannot find urpmi, looking for %s' % URPMI_PATH))
    p = module.params
    force_yes = p['force']
    no_recommends_yes = p['no_recommends']
    root = p['root']
    if p['update_cache']:
        update_package_db(module)
    packages = p['package'].split(',')
    if (p['state'] in ['installed', 'present']):
        install_packages(module, packages, root, force_yes, no_recommends_yes)
    elif (p['state'] in ['removed', 'absent']):
        remove_packages(module, packages, root)