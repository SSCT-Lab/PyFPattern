def remove_packages(module, names):
    installed = []
    for name in names:
        if query_package(module, name):
            installed.append(name)
    if (not installed):
        module.exit_json(changed=False, msg='package(s) already removed')
    names = ' '.join(installed)
    if module.check_mode:
        cmd = ('%s del --purge --simulate %s' % (APK_PATH, names))
    else:
        cmd = ('%s del --purge %s' % (APK_PATH, names))
    (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
    packagelist = parse_for_packages(stdout)
    if (rc != 0):
        module.fail_json(msg=('failed to remove %s package(s)' % names), stdout=stdout, stderr=stderr, packages=packagelist)
    module.exit_json(changed=True, msg=('removed %s package(s)' % names), stdout=stdout, stderr=stderr, packages=packagelist)