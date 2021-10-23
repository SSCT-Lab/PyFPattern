def install(m, pkgspec, cache, upgrade=False, default_release=None, install_recommends=None, force=False, dpkg_options=expand_dpkg_options(DPKG_OPTIONS), build_dep=False, autoremove=False, only_upgrade=False, allow_unauthenticated=False):
    pkg_list = []
    packages = ''
    pkgspec = expand_pkgspec_from_fnmatches(m, pkgspec, cache)
    package_names = []
    for package in pkgspec:
        if build_dep:
            pkg_list.append(("'%s'" % package))
            continue
        (name, version) = package_split(package)
        package_names.append(name)
        (installed, upgradable, has_files) = package_status(m, name, version, cache, state='install')
        if (((not installed) and (not only_upgrade)) or (upgrade and upgradable)):
            pkg_list.append(("'%s'" % package))
        if (installed and upgradable and version):
            pkg_list.append(("'%s'" % package))
    packages = ' '.join(pkg_list)
    if packages:
        if force:
            force_yes = '--force-yes'
        else:
            force_yes = ''
        if m.check_mode:
            check_arg = '--simulate'
        else:
            check_arg = ''
        if autoremove:
            autoremove = '--auto-remove'
        else:
            autoremove = ''
        if only_upgrade:
            only_upgrade = '--only-upgrade'
        else:
            only_upgrade = ''
        if build_dep:
            cmd = ('%s -y %s %s %s %s build-dep %s' % (APT_GET_CMD, dpkg_options, only_upgrade, force_yes, check_arg, packages))
        else:
            cmd = ('%s -y %s %s %s %s %s install %s' % (APT_GET_CMD, dpkg_options, only_upgrade, force_yes, autoremove, check_arg, packages))
        if default_release:
            cmd += (" -t '%s'" % (default_release,))
        if (install_recommends is False):
            cmd += ' -o APT::Install-Recommends=no'
        elif (install_recommends is True):
            cmd += ' -o APT::Install-Recommends=yes'
        if allow_unauthenticated:
            cmd += ' --allow-unauthenticated'
        (rc, out, err) = m.run_command(cmd)
        if m._diff:
            diff = parse_diff(out)
        else:
            diff = {
                
            }
        status = True
        data = dict(changed=True, stdout=out, stderr=err, diff=diff)
        if rc:
            status = False
            data = dict(msg=("'%s' failed: %s" % (cmd, err)), stdout=out, stderr=err, rc=rc)
    else:
        status = True
        data = dict(changed=False)
    if (not build_dep):
        mark_installed_manually(m, package_names)
    return (status, data)