

def main():
    module = AnsibleModule(argument_spec=dict(state=dict(type='str', default='installed', choices=['absent', 'installed', 'present', 'removed']), update_cache=dict(type='bool', default=False, aliases=['update-cache']), force=dict(type='bool', default=True), no_recommends=dict(type='bool', default=True, aliases=['no-recommends']), name=dict(type='list', required=True, aliases=['package', 'pkg']), root=dict(type='str', aliases=['installroot'])))
    p = module.params
    force_yes = p['force']
    no_recommends_yes = p['no_recommends']
    root = p['root']
    if p['update_cache']:
        update_package_db(module)
    packages = p['package']
    if (p['state'] in ['installed', 'present']):
        install_packages(module, packages, root, force_yes, no_recommends_yes)
    elif (p['state'] in ['removed', 'absent']):
        remove_packages(module, packages, root)
