def expand_pkgspec_from_fnmatches(m, pkgspec, cache):
    new_pkgspec = []
    if pkgspec:
        for pkgspec_pattern in pkgspec:
            (pkgname_pattern, version) = package_split(pkgspec_pattern)
            if frozenset('*?[]!').intersection(pkgname_pattern):
                if (':' not in pkgname_pattern):
                    try:
                        pkg_name_cache = _non_multiarch
                    except NameError:
                        pkg_name_cache = _non_multiarch = [pkg.name for pkg in cache if (':' not in pkg.name)]
                else:
                    try:
                        pkg_name_cache = _all_pkg_names
                    except NameError:
                        pkg_name_cache = _all_pkg_names = [pkg.name for pkg in cache]
                matches = fnmatch.filter(pkg_name_cache, pkgname_pattern)
                if (len(matches) == 0):
                    m.fail_json(msg=("No package(s) matching '%s' available" % str(pkgname_pattern)))
                else:
                    new_pkgspec.extend(matches)
            else:
                new_pkgspec.append(pkgspec_pattern)
    return new_pkgspec