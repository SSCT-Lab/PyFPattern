def _is_present(name, version, installed_pkgs, pkg_command):
    'Return whether or not package is installed.'
    for pkg in installed_pkgs:
        if ('==' in pkg):
            (pkg_name, pkg_version) = pkg.split('==')
        else:
            continue
        if ((pkg_name == name) and ((version is None) or (version == pkg_version))):
            return True
    return False