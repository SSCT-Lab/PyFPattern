def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='list', aliases=['package', 'pkg']), state=dict(type='str', default='present', choices=['absent', 'installed', 'latest', 'present', 'removed']), recurse=dict(type='bool', default=False), force=dict(type='bool', default=False), upgrade=dict(type='bool', default=False), update_cache=dict(type='bool', default=False, aliases=['update-cache'])), required_one_of=[['name', 'update_cache', 'upgrade']], supports_check_mode=True)
    pacman_path = module.get_bin_path('pacman', True)
    p = module.params
    if (p['state'] in ['present', 'installed']):
        p['state'] = 'present'
    elif (p['state'] in ['absent', 'removed']):
        p['state'] = 'absent'
    if (p['update_cache'] and (not module.check_mode)):
        update_package_db(module, pacman_path)
        if (not (p['name'] or p['upgrade'])):
            module.exit_json(changed=True, msg='Updated the package master lists')
    if (p['update_cache'] and module.check_mode and (not (p['name'] or p['upgrade']))):
        module.exit_json(changed=True, msg='Would have updated the package cache')
    if p['upgrade']:
        upgrade(module, pacman_path)
    if p['name']:
        pkgs = expand_package_groups(module, pacman_path, p['name'])
        pkg_files = []
        for (i, pkg) in enumerate(pkgs):
            if (not pkg):
                continue
            elif re.match('.*\\.pkg\\.tar(\\.(gz|bz2|xz|lrz|lzo|Z))?$', pkg):
                pkg_files.append(pkg)
                pkgs[i] = re.sub('-[0-9].*$', '', pkgs[i].split('/')[(- 1)])
            else:
                pkg_files.append(None)
        if module.check_mode:
            check_packages(module, pacman_path, pkgs, p['state'])
        if (p['state'] in ['present', 'latest']):
            install_packages(module, pacman_path, p['state'], pkgs, pkg_files)
        elif (p['state'] == 'absent'):
            remove_packages(module, pacman_path, pkgs)