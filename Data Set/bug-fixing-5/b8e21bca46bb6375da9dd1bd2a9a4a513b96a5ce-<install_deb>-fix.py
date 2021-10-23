def install_deb(m, debs, cache, force, install_recommends, allow_unauthenticated, dpkg_options):
    changed = False
    deps_to_install = []
    pkgs_to_install = []
    for deb_file in debs.split(','):
        try:
            pkg = apt.debfile.DebPackage(deb_file)
            pkg_name = get_field_of_deb(m, deb_file, 'Package')
            pkg_version = get_field_of_deb(m, deb_file, 'Version')
            if (len(apt_pkg.get_architectures()) > 1):
                pkg_arch = get_field_of_deb(m, deb_file, 'Architecture')
                pkg_key = ('%s:%s' % (pkg_name, pkg_arch))
            else:
                pkg_key = pkg_name
            try:
                installed_pkg = apt.Cache()[pkg_key]
                installed_version = installed_pkg.installed.version
                if (package_version_compare(pkg_version, installed_version) == 0):
                    continue
            except Exception:
                pass
            if ((not pkg.check()) and (not force)):
                m.fail_json(msg=pkg._failure_string)
            deps_to_install.extend(pkg.missing_deps)
        except Exception:
            e = get_exception()
            m.fail_json(msg=('Unable to install package: %s' % str(e)))
        pkgs_to_install.append(deb_file)
    retvals = {
        
    }
    if deps_to_install:
        (success, retvals) = install(m=m, pkgspec=deps_to_install, cache=cache, install_recommends=install_recommends, dpkg_options=expand_dpkg_options(dpkg_options))
        if (not success):
            m.fail_json(**retvals)
        changed = retvals.get('changed', False)
    if pkgs_to_install:
        options = ' '.join([('--%s' % x) for x in dpkg_options.split(',')])
        if m.check_mode:
            options += ' --simulate'
        if force:
            options += ' --force-all'
        cmd = ('dpkg %s -i %s' % (options, ' '.join(pkgs_to_install)))
        (rc, out, err) = m.run_command(cmd)
        if ('stdout' in retvals):
            stdout = (retvals['stdout'] + out)
        else:
            stdout = out
        if ('diff' in retvals):
            diff = retvals['diff']
            if ('prepared' in diff):
                diff['prepared'] += ('\n\n' + out)
        else:
            diff = parse_diff(out)
        if ('stderr' in retvals):
            stderr = (retvals['stderr'] + err)
        else:
            stderr = err
        if (rc == 0):
            m.exit_json(changed=True, stdout=stdout, stderr=stderr, diff=diff)
        else:
            m.fail_json(msg=('%s failed' % cmd), stdout=stdout, stderr=stderr)
    else:
        m.exit_json(changed=changed, stdout=retvals.get('stdout', ''), stderr=retvals.get('stderr', ''), diff=retvals.get('diff', ''))