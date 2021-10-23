

def install_packages(module, names, state):
    upgrade = False
    to_install = []
    to_upgrade = []
    for name in names:
        if query_virtual(module, name):
            dependencies = get_dependencies(module, name)
            for dependency in dependencies:
                if ((state == 'latest') and (not query_latest(module, dependency))):
                    to_upgrade.append(dependency)
        elif (not query_package(module, name)):
            to_install.append(name)
        elif ((state == 'latest') and (not query_latest(module, name))):
            to_upgrade.append(name)
    if to_upgrade:
        upgrade = True
    if ((not to_install) and (not upgrade)):
        module.exit_json(changed=False, msg='package(s) already installed')
    packages = (' '.join(to_install) + ' '.join(to_upgrade))
    if upgrade:
        if module.check_mode:
            cmd = ('%s add --upgrade --simulate %s' % (APK_PATH, packages))
        else:
            cmd = ('%s add --upgrade %s' % (APK_PATH, packages))
    elif module.check_mode:
        cmd = ('%s add --simulate %s' % (APK_PATH, packages))
    else:
        cmd = ('%s add %s' % (APK_PATH, packages))
    (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
    packagelist = parse_for_packages(stdout)
    if (rc != 0):
        module.fail_json(msg=('failed to install %s' % packages), stdout=stdout, stderr=stderr, packages=packagelist)
    module.exit_json(changed=True, msg=('installed %s package(s)' % packages), stdout=stdout, stderr=stderr, packages=packagelist)
