

def install_packages(module, packages, use_packages):
    install_c = 0
    portinstall_path = module.get_bin_path('portinstall', False)
    if (not portinstall_path):
        pkg_path = module.get_bin_path('pkg', False)
        if pkg_path:
            module.run_command('pkg install -y portupgrade')
        portinstall_path = module.get_bin_path('portinstall', True)
    if (use_packages == 'yes'):
        portinstall_params = '--use-packages'
    else:
        portinstall_params = ''
    for package in packages:
        if query_package(module, package):
            continue
        matches = matching_packages(module, package)
        if (matches == 1):
            (rc, out, err) = module.run_command(('%s --batch %s %s' % (portinstall_path, portinstall_params, package)))
            if (not query_package(module, package)):
                module.fail_json(msg=('failed to install %s: %s' % (package, out)))
        elif (matches == 0):
            module.fail_json(msg=('no matches for package %s' % package))
        else:
            module.fail_json(msg=('%s matches found for package name %s' % (matches, package)))
        install_c += 1
    if (install_c > 0):
        module.exit_json(changed=True, msg=('present %s package(s)' % install_c))
    module.exit_json(changed=False, msg='package(s) already present')
