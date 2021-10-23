def remove(m, pkgspec, cache, purge=False, force=False, dpkg_options=expand_dpkg_options(DPKG_OPTIONS), autoremove=False):
    pkg_list = []
    pkgspec = expand_pkgspec_from_fnmatches(m, pkgspec, cache)
    for package in pkgspec:
        (name, version) = package_split(package)
        (installed, upgradable, has_files) = package_status(m, name, version, cache, state='remove')
        if (installed or (has_files and purge)):
            pkg_list.append(("'%s'" % package))
    packages = ' '.join(pkg_list)
    if (len(packages) == 0):
        m.exit_json(changed=False)
    else:
        if force:
            force_yes = '--force-yes'
        else:
            force_yes = ''
        if purge:
            purge = '--purge'
        else:
            purge = ''
        if autoremove:
            autoremove = '--auto-remove'
        else:
            autoremove = ''
        if m.check_mode:
            check_arg = '--simulate'
        else:
            check_arg = ''
        cmd = ('%s -q -y %s %s %s %s %s remove %s' % (APT_GET_CMD, dpkg_options, purge, force_yes, autoremove, check_arg, packages))
        (rc, out, err) = m.run_command(cmd)
        if m._diff:
            diff = parse_diff(out)
        else:
            diff = {
                
            }
        if rc:
            m.fail_json(msg=("'apt-get remove %s' failed: %s" % (packages, err)), stdout=out, stderr=err, rc=rc)
        m.exit_json(changed=True, stdout=out, stderr=err, diff=diff)