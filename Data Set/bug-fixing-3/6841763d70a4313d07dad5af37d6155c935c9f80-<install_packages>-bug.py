def install_packages(module, pkgspec, force=True, no_recommends=True):
    packages = ''
    for package in pkgspec:
        if (not query_package_provides(module, package)):
            packages += ("'%s' " % package)
    if (len(packages) != 0):
        if no_recommends:
            no_recommends_yes = '--no-recommends'
        else:
            no_recommends_yes = ''
        if force:
            force_yes = '--force'
        else:
            force_yes = ''
        cmd = ('%s --auto %s --quiet %s %s' % (URPMI_PATH, force_yes, no_recommends_yes, packages))
        (rc, out, err) = module.run_command(cmd)
        installed = True
        for packages in pkgspec:
            if (not query_package_provides(module, package)):
                installed = False
        if (rc or (not installed)):
            module.fail_json(msg=("'urpmi %s' failed: %s" % (packages, err)))
        else:
            module.exit_json(changed=True, msg=('%s present(s)' % packages))
    else:
        module.exit_json(changed=False)