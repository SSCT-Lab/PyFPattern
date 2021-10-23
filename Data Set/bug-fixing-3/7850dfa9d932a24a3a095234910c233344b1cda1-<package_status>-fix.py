def package_status(m, pkgname, version, cache, state):
    try:
        pkg = cache[pkgname]
        ll_pkg = cache._cache[pkgname]
    except KeyError:
        if (state == 'install'):
            try:
                provided_packages = cache.get_providing_packages(pkgname)
                if provided_packages:
                    is_installed = False
                    upgradable = False
                    version_ok = False
                    if (cache.is_virtual_package(pkgname) and (len(provided_packages) == 1)):
                        package = provided_packages[0]
                        (installed, version_ok, upgradable, has_files) = package_status(m, package.name, version, cache, state='install')
                        if installed:
                            is_installed = True
                    return (is_installed, version_ok, upgradable, False)
                m.fail_json(msg=("No package matching '%s' is available" % pkgname))
            except AttributeError:
                return (False, False, True, False)
        else:
            return (False, False, False, False)
    try:
        has_files = (len(pkg.installed_files) > 0)
    except UnicodeDecodeError:
        has_files = True
    except AttributeError:
        has_files = False
    try:
        package_is_installed = (ll_pkg.current_state == apt_pkg.CURSTATE_INSTALLED)
    except AttributeError:
        try:
            package_is_installed = pkg.is_installed
        except AttributeError:
            package_is_installed = pkg.isInstalled
    version_is_installed = package_is_installed
    if version:
        versions = package_versions(pkgname, pkg, cache._cache)
        avail_upgrades = fnmatch.filter(versions, version)
        if package_is_installed:
            try:
                installed_version = pkg.installed.version
            except AttributeError:
                installed_version = pkg.installedVersion
            version_is_installed = fnmatch.fnmatch(installed_version, version)
            package_is_upgradable = False
            for candidate in avail_upgrades:
                if (package_version_compare(candidate, installed_version) > 0):
                    package_is_upgradable = True
                    break
        else:
            package_is_upgradable = bool(avail_upgrades)
    else:
        try:
            package_is_upgradable = pkg.is_upgradable
        except AttributeError:
            package_is_upgradable = pkg.isUpgradable
    return (package_is_installed, version_is_installed, package_is_upgradable, has_files)